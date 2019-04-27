"""
A way to launch numerous Jenkins masters and jobs with pytest.

From the CLI, this can be run as follows:
    $ PYTEST_ARGS="--masters=3 --jobs=10" ./test.sh -m scale jenkins
To specify a CPU quota (what JPMC does) then run:
    $ PYTEST_ARGS="--masters=3 --jobs=10 --cpu-quota=10.0" ./test.sh -m scale jenkins
To enable single use:
    $ PYTEST_ARGS="--masters=3 --jobs=10 --single-use" ./test.sh -m scale jenkins
And to clean-up a test run of Jenkins instances:
    $ ./test.sh -m scalecleanup jenkins

This supports the following configuration params:
    * Number of Jenkins masters (--masters)
    * Number of jobs for each master (--jobs); this will be the same
        count on each Jenkins instance. --jobs=10 will create 10 jobs
        on each instance.
    * How often, in minutes, to run a job (--run-delay); this is used
        to create a cron schedule: "*/run-delay * * * *"
    * To enable or disable "Mesos Single-Use Agent"; this is a toggle
        and applies to all jobs equally. (default: False)
    * How long, in seconds, for a job to "work" (sleep)
        (--work-duration)
    * CPU quota (--cpu-quota); 0.0 to disable / no quota
    * Memory quota (--memory-quota); 0.0 to disable / no quota
    * To enable or disable External Volumes (--external-volume);
        this uses rexray (default: False)
    * What test scenario to run (--scenario); supported values:
        - sleep (sleep for --work-duration)
        - buildmarathon (build the open source marathon project)
"""

import logging
import time
from threading import Thread, Lock
from typing import List, Set
from xml.etree import ElementTree

import config
import jenkins
import pytest
import sdk_dcos
import sdk_marathon
import sdk_quota
import sdk_security
import sdk_utils
import shakedown
import json

from tools import dcos_login
from sdk_dcos import DCOS_SECURITY

log = logging.getLogger(__name__)

SHARED_ROLE = "jenkins-role"
DOCKER_IMAGE="mesosphere/jenkins-dind:scale"
# initial timeout waiting on deployments
DEPLOY_TIMEOUT = 30 * 60  # 30 mins
JOB_RUN_TIMEOUT = 10 * 60  # 10 mins
SERVICE_ACCOUNT_TIMEOUT = 15 * 60 # 15 mins

LOCK = Lock()

TIMINGS = {"deployments": {}, "serviceaccounts": {}}
ACCOUNTS = {}


class ResultThread(Thread):
    """A thread that stores the result of the run command."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._result = None
        self._event = None

    @property
    def result(self) -> bool:
        """Run result

        Returns: True if completed successfully.

        """
        return bool(self._result)

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, event):
        self._event = event

    def run(self) -> None:
        start = time.time()
        try:
            super().run()
            self._result = True
        except Exception as e:
            self._result = False
        finally:
            end = time.time()
            if self.event:
                TIMINGS[self.event][self.name] = end - start


@pytest.mark.scale
def test_scaling_load(master_count,
                      job_count,
                      single_use: bool,
                      run_delay,
                      cpu_quota,
                      memory_quota,
                      work_duration,
                      mom,
                      external_volume: bool,
                      scenario,
                      min_index,
                      max_index,
                      batch_size) -> None:

    """Launch a load test scenario. This does not verify the results
    of the test, but does ensure the instances and jobs were created.

    The installation is run in threads, but the job creation and
    launch is then done serially after all Jenkins instances have
    completed installation.

    Args:
        master_count: Number of Jenkins masters or instances
        job_count: Number of Jobs on each Jenkins master
        single_use: Mesos Single-Use Agent on (true) or off (false)
        run_delay: Jobs should run every X minute(s)
        cpu_quota: CPU quota (0.0 to disable)
        work_duration: Time, in seconds, for generated jobs to sleep
        mom: Marathon on Marathon instance name
        external_volume: External volume on rexray (true) or local volume (false)
        min_index: minimum index to begin jenkins suffixes at
        max_index: maximum index to end jenkins suffixes at
        batch_size: batch size to deploy jenkins instances in
    """
    security_mode = sdk_dcos.get_security_mode()
    if mom and cpu_quota != 0.0 and memory_quota != 0.0:
        with shakedown.marathon_on_marathon(mom):
            _setup_quota(SHARED_ROLE, cpu_quota, memory_quota)

    # create marathon client
    if mom:
        with shakedown.marathon_on_marathon(mom):
            marathon_client = shakedown.marathon.create_client()
    else:
        marathon_client = shakedown.marathon.create_client()

    masters = []
    if min_index == -1 or max_index == -1:
        masters = ["jenkins{}".format(sdk_utils.random_string()) for _ in
                   range(0, int(master_count))]
    else:
        #max and min indexes are specified
        #NOTE: using min/max will override master count
        masters = ["jenkins{}".format(index) for index in
                    range(min_index, max_index)]
    # create service accounts in parallel
    sdk_security.install_enterprise_cli()

    if mom:
        _configure_admin_router(mom, SHARED_ROLE)

    current = 0
    end = max_index - min_index
    for current in range(0, end, batch_size):

        batched_masters = masters[current:current+batch_size]
        service_account_threads = _spawn_threads(batched_masters,
                                                _create_service_accounts,
                                                security=security_mode)

        thread_failures = _wait_and_get_failures(service_account_threads,
                                                 timeout=SERVICE_ACCOUNT_TIMEOUT)

        current = current + batch_size


# launch Jenkins services
    current = 0
    end = max_index - min_index
    for current in range(0, end, batch_size):

        log.info("Re-authenticating current batch load of jenkins{} - jenkins{} "
                 "to prevent auth-timeouts on scale cluster.".format(current, current+batch_size))
        dcos_login.login_session()

        batched_masters = masters[current:current+batch_size]
        install_threads = _spawn_threads(batched_masters,
                                         _install_jenkins,
                                         event='deployments',
                                         client=marathon_client,
                                         external_volume=external_volume,
                                         security=security_mode,
                                         daemon=True,
                                         mom=mom)
        thread_failures = _wait_and_get_failures(install_threads,
                                                 timeout=DEPLOY_TIMEOUT)
        thread_names = [x.name for x in thread_failures]

        # the rest of the commands require a running Jenkins instance
        deployed_masters = [x for x in batched_masters if x not in thread_names]
        job_threads = _spawn_threads(deployed_masters,
                                     _create_jobs,
                                     jobs=job_count,
                                     single=single_use,
                                     delay=run_delay,
                                     duration=work_duration,
                                     scenario=scenario)
        _wait_on_threads(job_threads, JOB_RUN_TIMEOUT)
        r = json.dumps(TIMINGS)
        print(r)
        current = current + batch_size


@pytest.mark.scalecleanup
def test_cleanup_scale(mom, min_index, max_index,service_id_list) -> None:
    """
     Args:
        mom: Marathon on Marathon instance name
        min_index: minimum index to begin jenkins suffixes at
        max_index: maximum index to end jenkins suffixes at
        service_id_list: list of service ids to delete

    Blanket clean-up of jenkins instances on a DC/OS cluster.
    1. Delete list of service ids if specified
    2. Delete range between max and min if specified
    1. Queries MoM for all apps matching "jenkins" prefix
    2. Delete all jobs on running Jenkins instances
    3. Uninstall all found Jenkins installs
    """
    service_ids = list()

    if service_id_list != '':
        service_ids = service_id_list.split(",")
    elif min_index != -1 and max_index != -1:
         service_ids = ["/jenkins{}".format(index) for index in
                    range(min_index, max_index)]
    else:
        r = sdk_marathon.filter_apps_by_id('jenkins', mom)
        jenkins_apps = r.json()['apps']
        jenkins_ids = [x['id'] for x in jenkins_apps]

        for service_id in jenkins_ids:
            if service_id.startswith('/'):
                service_id = service_id[1:]
            # skip over '/jenkins' instance - not setup by tests
            if service_id == 'jenkins':
                continue
            service_ids.append(service_id)

    cleanup_threads = _spawn_threads(service_ids,
                                     _cleanup_jenkins_install,
                                     mom=mom,
                                     daemon=False)
    _wait_and_get_failures(cleanup_threads, timeout=JOB_RUN_TIMEOUT)


def _setup_quota(role, cpus, memory):
    current_quotas = sdk_quota.list_quotas()
    if "infos" not in current_quotas:
        _set_quota(role, cpus, memory)
        return

    match = False
    for quota in current_quotas["infos"]:
        if quota["role"] == role:
            match = True
            break

    if match:
        sdk_quota.remove_quota(role)
    _set_quota(role, cpus, memory)


def _set_quota(role, cpus, memory):
    sdk_quota.create_quota(role, cpus=cpus, mem=memory)


def _spawn_threads(names, target, daemon=False, event=None, **kwargs) -> List[ResultThread]:
    """Create and start threads running target. This will pass
    the thread name to the target as the first argument.

    Args:
        names: Thread names
        target: Function to run in thread
        **kwargs: Keyword args for target

    Returns:
        List of threads handling target.
    """
    thread_list = list()
    for service_name in names:
        # setDaemon allows the main thread to exit even if
        # these threads are still running.
        t = ResultThread(target=target,
                         daemon=daemon,
                         name=service_name,
                         args=(service_name,),
                         kwargs=kwargs)
        t.event = event
        thread_list.append(t)
        t.start()
    return thread_list


def _create_service_accounts(service_name, security=None):
    if security == DCOS_SECURITY.strict:
        try:
            start = time.time()
            log.info("Creating service accounts for '{}'"
                     .format(service_name))
            sa_name = "{}-principal".format(service_name)
            sa_secret = "jenkins-{}-secret".format(service_name)
            sdk_security.create_service_account(
                    sa_name, sa_secret, service_name)

            sdk_security.grant_permissions(
                    'root', '*', sa_name)

            sdk_security.grant_permissions(
                    'root', SHARED_ROLE, sa_name)
            end = time.time()
            ACCOUNTS[service_name] = {}
            ACCOUNTS[service_name]["sa_name"] = sa_name 
            ACCOUNTS[service_name]["sa_secret"] = sa_secret
            TIMINGS["serviceaccounts"][service_name] = end - start
        except Exception as e:
            log.warning("Error encountered while creating service account: {}".format(e))
            raise e


def _install_jenkins(service_name,
                     client=None,
                     security=None,
                     **kwargs):
    """Install Jenkins service.

    Args:
        service_name: Service Name or Marathon ID (same thing)
        client: Marathon client connection
        external_volume: Enable external volumes
    """
    def _wait_for_deployment(app_id, client):
        with LOCK:
            res = len(client.get_deployments(app_id)) == 0
        return res

    try:
        if security == DCOS_SECURITY.strict:
            kwargs['strict_settings'] = {
                'secret_name':  ACCOUNTS[service_name]["sa_secret"],
                'mesos_principal': ACCOUNTS[service_name]["sa_name"],
            }
            kwargs['service_user'] = 'root'

        log.info("Installing jenkins '{}'".format(service_name))
        jenkins.install(service_name,
                        client,
                        role=SHARED_ROLE,
                        fn=_wait_for_deployment,
                        **kwargs)
    except Exception as e:
        log.warning("Error encountered while installing Jenkins: {}".format(e))
        raise e


def _cleanup_jenkins_install(service_name, **kwargs):
    """Delete all jobs and uninstall Jenkins instance.

    Args:
        service_name: Service name or Marathon ID
    """
    if service_name.startswith('/'):
        service_name = service_name[1:]
    try:
        log.info("Removing all jobs on {}.".format(service_name))
        jenkins.delete_all_jobs(service_name, retry=False)
    finally:
        log.info("Uninstalling {}.".format(service_name))
        jenkins.uninstall(service_name,
                          package_name=config.PACKAGE_NAME,
                          **kwargs)


def _create_jobs(service_name, **kwargs):
    """Create jobs on deployed Jenkins instances.

    All functionality around creating jobs should go here.

    Args:
        service_name: Jenkins instance name
    """
    m_label = _create_executor_configuration(service_name)
    _launch_jobs(service_name, label=m_label, **kwargs)


def _create_executor_configuration(service_name: str) -> str:
    """Create a new Mesos Slave Info configuration with a random name.

    Args:
        service_name: Jenkins instance to add the label

    Returns: Random name of the new config created.

    """
    mesos_label = "mesos"
    jenkins.create_mesos_slave_node(mesos_label,
                                    service_name=service_name,
                                    dockerImage=DOCKER_IMAGE,
                                    executorCpus=0.3,
                                    executorMem=1800,
                                    idleTerminationMinutes=1,
                                    timeout_seconds=600)
    return mesos_label


def _launch_jobs(service_name: str,
                 jobs: int = 1,
                 single: bool = False,
                 delay: int = 3,
                 duration: int = 600,
                 label: str = None,
                 scenario: str = None):
    """Create configured number of jobs with given config on Jenkins
    instance identified by `service_name`.

    Args:
        service_name: Jenkins service name
        jobs: Number of jobs to create and run
        single: Single Use Mesos agent on (true) or off
        delay: A job should run every X minute(s)
        duration: Time, in seconds, for the job to sleep
        label: Mesos label for jobs to use
    """
    job_name = 'generator-job'
    single_use_str = '100' if single else '0'

    seed_config_xml = jenkins._get_job_fixture('gen-job.xml')
    seed_config_str = ElementTree.tostring(
            seed_config_xml.getroot(),
            encoding='utf8',
            method='xml')
    jenkins.create_seed_job(service_name, job_name, seed_config_str)
    log.info(
            "Launching {} jobs every {} minutes with single-use "
            "({}).".format(jobs, delay, single))

    jenkins.run_job(service_name,
                    job_name,
                    timeout_seconds=600,
                    **{'JOBCOUNT':       str(jobs),
                       'AGENT_LABEL':    label,
                       'SINGLE_USE':     single_use_str,
                       'EVERY_XMIN':     str(delay),
                       'SLEEP_DURATION': str(duration),
                       'SCENARIO':       scenario})


def _wait_on_threads(thread_list: List[Thread],
                     timeout=DEPLOY_TIMEOUT) -> List[Thread]:
    """Wait on the threads in `install_threads` until a specified time
    has elapsed.

    Args:
        thread_list: List of threads
        timeout: Timeout is seconds

    Returns:
        List of threads that are still running.

    """
    start_time = current_time = time.time()
    for thread in thread_list:
        remaining = timeout - (current_time - start_time)
        if remaining < 1:
            break
        thread.join(timeout=remaining)
        current_time = time.time()
    active_threads = [x for x in thread_list if x.isAlive()]
    return active_threads


def _wait_and_get_failures(thread_list: List[ResultThread],
                           **kwargs) -> Set[Thread]:
    """Wait on threads to complete or timeout and log errors.

    Args:
        thread_list: List of threads to wait on

    Returns: A list of service names that failed or timed out.

    """
    timeout_failures = _wait_on_threads(thread_list, **kwargs)
    timeout_names = [x.name for x in timeout_failures]
    if timeout_names:
        log.warning("The following {:d} Jenkins instance(s) failed to "
                    "complete in {:d} minutes: {}"
                    .format(len(timeout_names),
                            DEPLOY_TIMEOUT // 60,
                            ', '.join(timeout_names)))
    # the following did not timeout, but failed
    run_failures = [x for x in thread_list if not x.result]
    run_fail_names = [x.name for x in run_failures]
    if run_fail_names:
        log.warning("The following {:d} Jenkins instance(s) "
                    "encountered an error: {}"
                    .format(len(run_fail_names),
                            ', '.join(run_fail_names)))
    return set(timeout_failures + run_failures)


def _configure_admin_router(mom_role, jenkins_role=SHARED_ROLE):
    # Admin-Router by default only has permissions to read from '*' and 'slave_public' roles.
    # When jenkins is launched on a MoM it runs under the mom role.
    # Here we explicily grant Admin-Router access to both jenkins-role and mom roles.
    
    ADMIN_ROUTER_SERVICE_ACCOUNT_NAME='dcos_adminrouter' 

    permissions = [ 
        {
            'user': ADMIN_ROUTER_SERVICE_ACCOUNT_NAME,
            'acl': "dcos:mesos:master:framework:role:{}".format(jenkins_role),
            'description': "Grant Admin-Router access to services with the role {}".format(jenkins_role),
            'action': 'read'
        },
        {
            'user': ADMIN_ROUTER_SERVICE_ACCOUNT_NAME,
            'acl': "dcos:mesos:master:framework:role:{}".format(mom_role),
            'description': "Grant Admin-Router access to services with the role {}".format(mom_role),
            'action': 'read'
        }
    ]
    
    log.info("Granting permissions to {}".format(ADMIN_ROUTER_SERVICE_ACCOUNT_NAME))
    for permission in permissions:
        sdk_security.grant(**permission)
    log.info("Permission setup completed for {}".format(ADMIN_ROUTER_SERVICE_ACCOUNT_NAME))

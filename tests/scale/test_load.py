"""
A way to launch numerous Jenkins masters and jobs with pytest.

From the CLI, this can be run as follows:
    $ PYTEST_ARGS="--masters=3 --jobs=10" ./test.sh -m scale jenkins
To specify a CPU quota (what JPMC does) then run:
    $ PYTEST_ARGS="--masters=3 --jobs=10 --cpu-quota=10.0" ./test.sh -m scale jenkins
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
        and applies to all jobs equally.
    * How long, in seconds, for a job to "work" (sleep)
        (--work-duration)
    * CPU quota (--cpu-quota); 0.0 to disable / no quota
"""

import logging
import threading
from xml.etree import ElementTree

import config
import jenkins
import pytest
import sdk_marathon
import sdk_quota
import sdk_utils
import shakedown

log = logging.getLogger(__name__)

SHARED_ROLE = "jenkins-role"


@pytest.mark.scale
def test_scaling_load(master_count,
                      job_count,
                      single_use,
                      run_delay,
                      cpu_quota,
                      work_duration,
                      mom):
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
    """
    with shakedown.marathon_on_marathon(mom):
        if cpu_quota is not 0.0:
            _setup_quota(SHARED_ROLE, cpu_quota)

    masters = ["jenkins{}".format(sdk_utils.random_string()) for _ in
               range(0, int(master_count))]
    # launch Jenkins services
    install_threads = list()
    for service_name in masters:
        t = threading.Thread(target=_install_jenkins,
                             args=(service_name, mom))
        install_threads.append(t)
        t.start()
    # wait on installation threads
    for thread in install_threads:
        thread.join()
    # now try to launch jobs
    for service_name in masters:
        m_label = _create_executor_configuration(service_name)
        _launch_jobs(service_name,
                     jobs=job_count,
                     single=single_use,
                     delay=run_delay,
                     duration=work_duration,
                     label=m_label)


@pytest.mark.scalecleanup
def test_cleanup_scale(mom):
    """Blanket clean-up of jenkins instances on a DC/OS cluster.

    1. Queries Marathon for all apps matching "jenkins" prefix
    2. Delete all jobs on running Jenkins instances
    3. Uninstall all found Jenkins installs
    """
    r = sdk_marathon.filter_apps_by_id('jenkins', mom)
    jenkins_apps = r.json()['apps']
    jenkins_ids = [x['id'] for x in jenkins_apps]

    cleanup_threads = list()
    for service_id in jenkins_ids:
        if service_id.startswith('/'):
            service_id = service_id[1:]
        # skip over '/jenkins' instance - not setup by tests
        if service_id == 'jenkins':
            continue
        t = threading.Thread(target=_cleanup_jenkins_install,
                             args=(service_id, mom))
        cleanup_threads.append(t)
        t.start()
    # wait for cleanup to complete
    for thread in cleanup_threads:
        thread.join()


def _setup_quota(role, cpus):
    current_quotas = sdk_quota.list_quotas()
    if "infos" not in current_quotas:
        _set_quota(role, cpus)
        return

    match = False
    for quota in current_quotas["infos"]:
        if quota["role"] == role:
            match = True
            break

    if match:
        sdk_quota.remove_quota(role)
    _set_quota(role, cpus)


def _set_quota(role, cpus):
    sdk_quota.create_quota(role, cpus=cpus)


def _install_jenkins(service_name, mom=None):
    """Install Jenkins service.

    Args:
        service_name: Service Name or Marathon ID (same thing)
    """
    log.info("Installing jenkins '{}'".format(service_name))
    jenkins.install(service_name, role=SHARED_ROLE, mom=mom)


def _cleanup_jenkins_install(service_name, mom=None):
    """Delete all jobs and uninstall Jenkins instance.

    Args:
        service_name: Service name or Marathon ID
    """
    if service_name.startswith('/'):
        service_name = service_name[1:]
    log.info("Removing all jobs on {}.".format(service_name))
    jenkins.delete_all_jobs(service_name, retry=False)
    log.info("Uninstalling {}.".format(service_name))
    jenkins.uninstall(service_name,
                      package_name=config.PACKAGE_NAME,
                      mom=mom)


def _create_executor_configuration(service_name):
    """Create a new Mesos Slave Info configuration with a random name.

    Args:
        service_name: Jenkins instance to add the label

    Returns: Random name of the new config created.

    """
    mesos_label = "mesos"
    jenkins.create_mesos_slave_node(mesos_label,
                                    service_name=service_name,
                                    executorCpus=0.3,
                                    executorMem=1800,
                                    idleTerminationMinutes=1)
    return mesos_label


def _launch_jobs(service_name: str,
                 jobs: int = 1,
                 single: bool = False,
                 delay: int = 3,
                 duration: int = 600,
                 label: str = None):
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

    single_use_str = '100'
    if not single or (
            type(single) == str and single.lower() == 'false'
    ):
        single_use_str = '0'

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
                    **{'JOBCOUNT':       str(jobs),
                       'AGENT_LABEL':    label,
                       'SINGLE_USE':     single_use_str,
                       'EVERY_XMIN':     str(delay),
                       'SLEEP_DURATION': str(duration)})

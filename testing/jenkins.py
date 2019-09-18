import logging
import os
from xml.etree import ElementTree

import jenkins_remote_access
import sdk_cmd
import sdk_install
from shakedown import *

TIMEOUT_SECONDS = 30 * 60
SHORT_TIMEOUT_SECONDS = 30

log = logging.getLogger(__name__)


def install(service_name, client,
            role=None,
            external_volume=None,
            strict_settings=None,
            service_user=None,
            fn=None,
            mom=None):
    """Install a Jenkins instance and set the service name to
    `service_name`. This does not wait for deployment to finish.

    Args:
        service_name: Unique service name
        client: Marathon client connection
        role: The role for the service to use (default is no role)
        external_volume: Enable external volumes
        strict_settings: Dictionary that contains the secret name and
            mesos principal to use in strict mode.
        service_user: user
        fn: Function to determine if install is complete
    """
    def _wait_for_deployment(app_id, client):
        return len(client.get_deployments(app_id)) == 0

    # use _wait_for_deployment if no function provided
    if not fn:
        fn = _wait_for_deployment

    options = {
        "service": {
            "name": service_name
        }
    }

    if role:
        options["roles"] = {
            "jenkins-agent-role": role
        }

    if external_volume:
        options["storage"] = {
            "external-persistent-volume-name": service_name
        }
    else:
        options["storage"] = {
            "local-persistent-volume-size": 1024
        }

    if strict_settings:
        options["security"] = {
            "secret-name": strict_settings['secret_name'],
            "strict-mode": True
        }

    if service_user:
        options['service']['user'] = service_user

    # get the package json for given options
    pkg_json = sdk_install.get_package_json('jenkins', None, options)
    if mom:
        pkg_json["env"]["MARATHON_NAME"] = mom
    client.add_app(pkg_json)
    time_wait(lambda: fn(service_name, client),
              TIMEOUT_SECONDS,
              sleep_seconds=20)


def uninstall(service_name, package_name='jenkins', role=None, mom=None):
    """Uninstall a Jenkins instance. This does not wait for deployment
     to finish.

    Args:
        service_name: Unique service name
        package_name: Package name to uninstall
        role: The role for the service to use (default is no role)
        mom: Marathon on Marathon service name
    """
    if mom:
        with marathon_on_marathon(mom):
            delete_app(service_name)
    else:
        sdk_install.uninstall(
            package_name,
            service_name,
            role=role)


def create_mesos_slave_node(
        labelString,
        service_name='jenkins',
        **kwargs
):
    # TODO check if the label exists and then create or else a NOOP.
    # create the mesos slave node with given label. LABEL SHOULD NOT PRE-EXIST.
    return jenkins_remote_access.add_slave_info(
        labelString,
        service_name=service_name,
        **kwargs
    )


def create_job(
        service_name,
        job_name,
        cmd="echo \"Hello World\"; sleep 30",
        schedule_frequency_in_min=1,
        labelString=None
):
    headers = {'Content-Type': 'application/xml'}
    svc_url = dcos_service_url(service_name)
    url = "{}createItem?name={}".format(svc_url, job_name)
    job_config = construct_job_config(cmd, schedule_frequency_in_min, labelString)

    r = http.post(url, headers=headers, data=job_config)

    return r


def create_seed_job(
        service_name,
        job_name,
        content
):
    url = "createItem?name={}".format(job_name)
    try:
        r = sdk_cmd.service_request(
            'POST',
            service_name,
            url,
            data=content,
            log_args=True,
            headers = {'Content-Type': 'application/xml'}
        )
        return r
    except Exception as inst:
        print(type(inst))
        print(inst)


def delete_all_jobs(service_name, retry=True):
    """Delete all jobs on a Jenkins instance.

    Args:
        service_name: Jenkins instance
        retry: Retry this request

    Returns: HTTP Response

    """
    return jenkins_remote_access.delete_all_jobs(
            service_name=service_name,
            retry=retry)


def construct_job_config(cmd, schedule_frequency_in_min, labelString):
    updated_job_config = _get_job_fixture('test-job.xml')

    cron = '*/{} * * * *'.format(schedule_frequency_in_min)
    updated_job_config.find('.//spec').text = cron
    updated_job_config.find('.//command').text = cmd
    if labelString:
        updated_job_config.find('.//assignedNode').text = labelString
    root = updated_job_config.getroot()
    xmlstr = ElementTree.tostring(root, encoding='utf8', method='xml')

    return xmlstr


def copy_job(service_name, src_name, dst_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    path = 'createItem?name={}&mode=copy&from={}'.format(dst_name, src_name)
    sdk_cmd.service_request('POST', service_name, path, timeout_seconds=timeout_seconds)

    # Copy starts jobs off disable and you have to disable them and enable again to get them "buildable"
    # https://github.com/entagen/jenkins-build-per-branch/issues/41
    disable_job(service_name, dst_name)
    enable_job(service_name, dst_name)


def run_job(service_name, job_name, timeout_seconds=SHORT_TIMEOUT_SECONDS, **kwargs):
    params = '&'.join(["{}={}".format(i[0], i[1]) for i in kwargs.items()])
    path = 'job/{}/buildWithParameters?{}'.format(job_name, params)
    return sdk_cmd.service_request('POST', service_name, path, timeout_seconds=timeout_seconds)


def enable_job(service_name, job_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return _set_buildable(service_name, job_name, True, timeout_seconds)


def disable_job(service_name, job_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return _set_buildable(service_name, job_name, False, timeout_seconds)


def _set_buildable(service_name, job_name, buildable, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    verb = None

    if buildable:
        verb = 'enable'
    else:
        verb = 'disable'

    path = 'job/{}/{}'.format(job_name, verb)
    return sdk_cmd.service_request('POST', service_name, path, timeout_seconds=timeout_seconds)


def get_jobs(service_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return _get_jenkins_root(service_name, timeout_seconds)['jobs']


def get_job(service_name, job_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    path = _get_jenkins_json_path(service_name, 'job/{}'.format(job_name))
    return _get_jenkins_json(service_name, path, timeout_seconds)


def get_builds(service_name, job_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return get_job(service_name, job_name)['builds']


def get_build(service_name, job_name, number, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    path = _get_jenkins_json_path(service_name, 'job/{}/{}'.format(job_name, number))
    return _get_jenkins_json(service_name, path, timeout_seconds)


def get_first_build(service_name, job_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return _get_named_build(service_name, job_name, 'firstBuild')


def get_last_build(service_name, job_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return _get_named_build(service_name, job_name, 'lastBuild')


def _get_named_build(service_name, job_name, build_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    last_build = get_job(service_name, job_name)[build_name]
    if last_build is None:
        return None

    return get_build(service_name, job_name, last_build['number'])


def _get_jenkins_root(service_name, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return _get_jenkins_json(service_name, 'api/json', timeout_seconds)


def _get_jenkins_json(service_name, path, timeout_seconds=SHORT_TIMEOUT_SECONDS):
    return sdk_cmd.service_request('GET', service_name, path, timeout_seconds=timeout_seconds).json()


def _get_jenkins_json_path(service_name, path):
    return '{}/api/json'.format(path)


def _get_job_fixture(job_name):
    """Get the XML of the job fixture `job_name`. This should include
    the file suffix.
    """
    here = os.path.dirname(__file__)
    return ElementTree.parse(os.path.join(here, 'testData', job_name))

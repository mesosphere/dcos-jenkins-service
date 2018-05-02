import logging
import uuid

import config
import jenkins
import jenkins_remote_access
import pytest
import retrying
import sdk_install
import sdk_utils

log = logging.getLogger(__name__)


@pytest.fixture(scope='module', autouse=True)
def configure_package():
    try:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
        sdk_install.install(config.PACKAGE_NAME, config.SERVICE_NAME, 0, wait_for_deployment=False)

        yield  # let the test session execute
    finally:
        pass
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)


@pytest.fixture
def create_slave() -> str:
    label = sdk_utils.random_string()
    jenkins.create_mesos_slave_node(label)
    r = jenkins.create_mesos_slave_node(label, service_name=config.SERVICE_NAME)
    assert r.status_code == 200, 'create_mesos_slave_node failed : {}'.format(
        r.status_code
    )
    assert label in r.text, 'Label {} missing from {}'.format(label, r.text)
    log.info("Set of labels is now: %s", r.text)
    yield label
    log.info("Removing label %s", label)
    r = jenkins_remote_access.remove_slave_info(
        label, service_name=config.SERVICE_NAME
    )
    assert r.status_code == 200, 'remove_slave_info failed : {}'.format(
        r.status_code
    )
    assert label not in r.text, 'Label {} still present in {}'.format(
        label, r.text
    )
    log.info("Set of labels is now: %s", r.text)


@pytest.mark.sanity
def test_create_job():
    test_job_name = get_test_job_name()
    jenkins.create_job(config.SERVICE_NAME, test_job_name, "echo \"test command\";", 5)
    job = jenkins.get_job(config.SERVICE_NAME, test_job_name)

    assert test_job_name == job['name']


@pytest.mark.sanity
def test_label_create_job(create_slave):
    test_job_name = get_test_job_name()
    jenkins.create_job(config.SERVICE_NAME, test_job_name, "echo \"test command\";", 1, create_slave)
    job = jenkins.get_job(config.SERVICE_NAME, test_job_name)

    assert test_job_name == job['name']
    wait_until_job_run(config.SERVICE_NAME, test_job_name)


@pytest.mark.sanity
def test_install_custom_name():
    svc_name = 'jenkins-custom'
    test_job_name = get_test_job_name()

    sdk_install.uninstall(config.PACKAGE_NAME, svc_name)

    try:
        jenkins.install(svc_name)
        jenkins.create_job(svc_name, test_job_name)
        job = jenkins.get_job(svc_name, test_job_name)
        assert test_job_name == job['name']
    finally:
        sdk_install.uninstall(config.PACKAGE_NAME, svc_name)


def get_test_job_name():
    return 'test-job-{}'.format(uuid.uuid4())


@retrying.retry(
    stop_max_delay=5 * 60 * 1000,
    wait_fixed=20 * 1000
)
def wait_until_job_run(service_name: str, job_name: str) -> None:
    last_build = jenkins.get_last_build(service_name, job_name)
    log.info(last_build)
    # TODO make this check strong if needed.
    assert last_build

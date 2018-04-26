import logging
import uuid

import config
import jenkins
import jenkins_remote_access
import pytest
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
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)


@pytest.fixture
def create_slave() -> str:
    label = sdk_utils.random_string()
    jenkins.create_mesos_slave_node(label)
    yield label
    jenkins_remote_access.remove_slave_info(label)


@pytest.mark.sanity
def test_create_job():
    test_job_name = get_test_job_name()
    jenkins.create_job(config.SERVICE_NAME, test_job_name, "echo \"test command\";", 5)
    job = jenkins.get_job(config.SERVICE_NAME, test_job_name)

    assert test_job_name == job['name']


@pytest.mark.sanity
def test_label_create_job(create_slave):
    test_job_name = get_test_job_name()
    jenkins.create_job(config.SERVICE_NAME, test_job_name, "echo \"test command\";", 5, create_slave)
    job = jenkins.get_job(config.SERVICE_NAME, test_job_name)

    assert test_job_name == job['name']


@pytest.mark.sanity
def test_jenkins_remote_access():
    rand_label = sdk_utils.random_string()
    r = jenkins_remote_access.add_slave_info(rand_label)
    assert r.status_code == 200, 'Got {} when trying to post MesosSlaveInfo'.format(r.status_code)
    r = jenkins_remote_access.remove_slave_info(rand_label)
    assert r.status_code == 200, 'Got {} when trying to remove label'.format(r.status_code)


@pytest.mark.sanity
def test_install_custom_name():
    svc_name = 'jenkins-custom'
    test_job_name = get_test_job_name()

    sdk_install.uninstall(config.PACKAGE_NAME, svc_name)

    try:
        jenkins.install(svc_name, 50001)
        jenkins.create_job(svc_name, test_job_name)
        job = jenkins.get_job(svc_name, test_job_name)

        assert test_job_name == job['name']
    finally:
        pass
        sdk_install.uninstall(config.PACKAGE_NAME, svc_name)


def get_test_job_name():
    return 'test-job-{}'.format(uuid.uuid4())

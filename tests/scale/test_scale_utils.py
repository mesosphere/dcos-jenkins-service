import logging
import pytest
import uuid

import config
import jenkins
import jenkins_remote_access
import sdk_install
import sdk_utils

log = logging.getLogger(__name__)

test_job_name = 'test-job-{}'.format(uuid.uuid4())


@pytest.fixture(scope='module', autouse=True)
def configure_package():
    try:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
        sdk_install.install(config.PACKAGE_NAME, config.SERVICE_NAME, 0, wait_for_deployment=False)

        yield  # let the test session execute
    finally:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)


@pytest.mark.sanity
def test_create_job():
    jenkins.create_job(config.SERVICE_NAME, test_job_name, "echo \"test command\";", 5)
    job = jenkins.get_job(config.SERVICE_NAME, test_job_name)

    assert test_job_name == job['name']


@pytest.mark.sanity
def test_jenkins_remote_access():
    rand_label = sdk_utils.random_string()
    r = jenkins_remote_access.add_slave_info(rand_label)
    assert r.status_code == 200, 'Got {} when trying to post MesosSlaveInfo'.format(r.status_code)
    r = jenkins_remote_access.remove_slave_info(rand_label)
    assert r.status_code == 200, 'Got {} when trying to remove label'.format(r.status_code)

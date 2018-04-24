import logging
import pytest
import uuid

import config
import jenkins
import sdk_install

log = logging.getLogger(__name__)

test_job_name = 'test-job-{}'.format(uuid.uuid4())

@pytest.fixture(scope='module', autouse=True)
def configure_package():
    try:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
        sdk_install.install(config.PACKAGE_NAME, config.SERVICE_NAME, 0, wait_for_deployment=False)

        yield # let the test session execute
    finally:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)


@pytest.mark.sanity
def test_create_job():
    jenkins.create_job(config.SERVICE_NAME, test_job_name, 5)
    job = jenkins.get_job(config.SERVICE_NAME, test_job_name)

    assert test_job_name == job['name']
    

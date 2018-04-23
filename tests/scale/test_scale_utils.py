import logging
import pytest
import uuid

import config
import jenkins
import sdk_install

log = logging.getLogger(__name__)

service_name = 'jenkins'

@pytest.fixture(scope='module', autouse=True)
def configure_package():
    try:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
        sdk_install.install(config.PACKAGE_NAME, config.SERVICE_NAME, 0, wait_for_deployment=False)
        jenkins.wait_for_jenkins_marathon_app_healthy(config.SERVICE_NAME, 3 * 60)

        yield # let the test session execute
    finally:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)


@pytest.mark.sanity
def test_get_builds():
    log.info('Getting Jenkins jobs')
    jobs = jenkins.get_jobs(service_name)
    log.info('jobs: {}'.format(jobs))

    for job in jobs:
        name = job['name']
        log.info('first build: {}'.format(jenkins.get_first_build(service_name, name)))
        log.info('last build: {}'.format(jenkins.get_last_build(service_name, name)))


@pytest.mark.sanity
def test_copy_job():
    for x in range(0, 100):
        copy_name = str(uuid.uuid4())
        jenkins.copy_job(service_name, 'test', copy_name)

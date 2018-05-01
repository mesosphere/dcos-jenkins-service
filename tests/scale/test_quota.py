import logging
import pytest
import uuid

import config
import sdk_install
import sdk_quota

log = logging.getLogger(__name__)


@pytest.fixture(scope='module', autouse=True)
def configure_package():
    try:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
        sdk_install.install(config.PACKAGE_NAME,
                            config.SERVICE_NAME, 0, wait_for_deployment=False,
                            additional_options={
                                "roles": {
                                    "jenkins-agent-role": "jenkins"
                                }
                            })

        yield  # let the test session execute
    finally:
        pass
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)


@pytest.mark.sanity
def test_create_quota():
    try:
        sdk_quota.create_quota("jenkins", cpus=4.0, mem=4000)
        quotas = sdk_quota.list_quotas()

        present = False
        for quota in quotas['infos']:
            if quota['role'] == "jenkins":
                present = True
                break

        assert present, "There was no quota present for the jenkins role"

    finally:
        sdk_quota.remove_quota("jenkins")

        quotas = sdk_quota.list_quotas()
        if 'infos' in quotas:
            for quota in quotas['infos']:
                assert quota['role'] != "jenkins"

"""Jenkins acceptance tests for DC/OS."""

from shakedown import *

PACKAGE_NAME = 'jenkins'
JOB_NAME = 'jenkins-acceptance-test-job'
DCOS_SERVICE_URL = dcos_service_url(PACKAGE_NAME)
WAIT_TIME_IN_SECS = 300


def test_install_jenkins():
    """Install the Jenkins package for DC/OS.
    """
    client = shakedown.marathon.create_client()
    install_package_and_wait(PACKAGE_NAME, client)
    assert package_installed(PACKAGE_NAME), 'Package failed to install'

    end_time = time.time() + WAIT_TIME_IN_SECS
    found = False
    while time.time() < end_time:
        found = get_service(PACKAGE_NAME) is not None
        if found and service_healthy(PACKAGE_NAME):
            break
        time.sleep(1)

    assert found, 'Service did not register with DCOS'


def test_jenkins_is_alive():
    """Ensure Jenkins is alive by attempting to get the version from the
    Jenkins master, which is present in the HTTP headers.
    """
    end_time = time.time() + WAIT_TIME_IN_SECS
    while time.time() < end_time:
        try:
            # This can except on a 500 until the Jenkins app has started
            r = http.get(DCOS_SERVICE_URL)
            if r.status_code < 500:
                assert r.status_code == 200, 'Did not receive HTTP 200 OK status code'
                assert 'X-Jenkins' in r.headers, 'Missing the X-Jenkins HTTP header.'
                break
        except:
            pass
        time.sleep(1)


def test_create_a_job():
    """Create a new Jenkins job.
    """
    here = os.path.dirname(__file__)
    headers = {'Content-Type': 'application/xml'}
    job_config = ''
    url = "{}/createItem?name={}".format(DCOS_SERVICE_URL, JOB_NAME)

    with open(os.path.join(here, 'fixtures', 'test-job.xml')) as test_job:
        job_config = test_job.read()

    r = http.post(url, headers=headers, data=job_config)
    assert r.status_code == 200, 'Failed to create test job.'


def test_trigger_a_job_build():
    """Build the new Jenkins job we've created.
    """
    url = "{}/job/{}/build".format(DCOS_SERVICE_URL, JOB_NAME)
    r = http.post(url)

    assert r.status_code == 201, 'Failed to build tet job.'


def test_wait_for_jenkins_build_agent():
    """A dynamic build agent needs to connect before the build can kick off.
    """
    success = False
    end_time = time.time() + WAIT_TIME_IN_SECS
    while time.time() < end_time:
       if get_service_tasks('jenkins'):
           success = True
           break
       time.sleep(5)

    assert success, 'Agent did not connect within allowed time.'


def test_wait_for_build_to_start():
    """Wait for the job we triggered to start.
    """
    success = False
    url = "{}/job/{}/1/api/json".format(DCOS_SERVICE_URL, JOB_NAME)
    end_time = time.time() + WAIT_TIME_IN_SECS
    while time.time() < end_time:
        try:
            # This can except on a 404 until the job is created on the build agent
            r = http.get(url)
            success = True
            break
        except:
            pass
        time.sleep(5)

    assert success, 'Build did not start within allowed time.'


def test_wait_for_build_to_finish():
    """Wait for the job we kicked off to finish.
    """
    success = False
    url = "{}/job/{}/1/api/json".format(DCOS_SERVICE_URL, JOB_NAME)
    end_time = time.time() + WAIT_TIME_IN_SECS
    while time.time() < end_time:
       r = http.get(url)

       if r.status_code == 200:
           data = r.json()
           if data['result'] in ('SUCCESS', 'FAILURE'):
               print(data['result'])
               success = True
               break
       time.sleep(5)

    assert success, 'Build did not finish within allowed time.'


def test_delete_a_job():
    """Delete our test job.
    """
    url = "{}/job/{}/doDelete".format(DCOS_SERVICE_URL, JOB_NAME)
    r = http.post(url)

    assert r.status_code == 200, 'Failed to delete test job.'


def test_uninstall_jenkins():
    """Uninstall the Jenkins package for DC/OS.
    """
    uninstall_package_and_wait(PACKAGE_NAME)
    assert not package_installed(PACKAGE_NAME), 'Package failed to uninstall'

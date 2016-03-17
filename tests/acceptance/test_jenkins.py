"""Jenkins acceptance tests for DCOS."""

from shakedown.dcos import *
from shakedown.dcos.package import *
from shakedown.dcos.service import *

PACKAGE_NAME = 'jenkins'
DCOS_SERVICE_URL = dcos_service_url(PACKAGE_NAME)
WAIT_TIME_IN_SECS = 300


def test_install_jenkins():
    """Install the Jenkins package for DCOS.
    """
    install_package_and_wait(PACKAGE_NAME)
    assert package_installed(PACKAGE_NAME), 'Package failed to install'

    end_time = time.time() + WAIT_TIME_IN_SECS
    found = False
    while time.time() < end_time:
        found = get_service(PACKAGE_NAME) is not None
        if found:
            break
        time.sleep(1)

    assert found, 'Service did not register with DCOS'


def test_jenkins_is_alive():
    """Ensure Jenkins is alive by attempting to get the version from the
    Jenkins master, which is present in the HTTP headers.
    """
    end_time = time.time() + WAIT_TIME_IN_SECS
    while time.time() < end_time:
        r = requests.get(DCOS_SERVICE_URL)
        # a 50x suggests the Jenkins service is still starting
        # so loop until that changes. Anything else is a problem.
        if r.status_code < 500:
            assert r.status_code == 200, 'Did not receive HTTP 200 OK status code'
            assert 'X-Jenkins' in r.headers, 'Missing the X-Jenkins HTTP header.'
            break
        time.sleep(1)


def test_create_and_build_a_job():
    """Create a new Jenkins job and add it to the build queue.
    """
    here = os.path.dirname(__file__)
    headers = {'Content-Type': 'application/xml'}
    job_name = 'jenkins-acceptance-test-job'
    job_config = ''
    url_strs = ("{}/createItem?name={}", "{}/job/{}/build", "{}/job/{}/1/api/json", "{}/job/{}/doDelete",
                "{}/job/{}/1/consoleText")
    url_names = ('create', 'build', 'status', 'delete', 'console_log')
    # this creates a dictionary of urls.
    # urls['create'] returns a populated "{}/createItem?name={}" URL
    urls = dict(zip(url_names, [i.format(DCOS_SERVICE_URL, job_name) for i in url_strs]))

    with open(os.path.join(here, 'fixtures', 'test-job.xml')) as test_job:
        job_config = test_job.read()

    r = requests.post(urls['create'], headers=headers, data=job_config)
    assert r.status_code == 200, 'Failed to create test job.'

    requests.post(urls['build'])

    # Query the API every second for two minutes; this should be more than
    # enough time for the build to complete given:
    #   * the test job sleeps for 30 seconds
    #   * it shouldn't take more than a minute to launch the container
    #   * an add'l 30 seconds for good measure
    build_result, console_log = None, None
    end_time = time.time() + WAIT_TIME_IN_SECS
    while time.time() < end_time:
        r = requests.get(urls['status'])
        if r.status_code == 200:
            data = r.json()
            build_result = data['result']
            if build_result == 'FAILURE':
                log = requests.get(urls['console_log'])
                console_log = log.text
            if build_result in ('SUCCESS', 'FAILURE'):
                break
        time.sleep(1)

    # delete job
    requests.post(urls['delete'])

    assert build_result is not None, 'Never received a HTTP 200 response from Jenkins.'
    assert build_result != 'FAILURE', "The Jenkins build failed. The console output follows:\n{}".format(console_log)


def test_uninstall_jenkins():
    """Uninstall the Jenkins package for DCOS.
    """
    uninstall_package(PACKAGE_NAME)
    assert not package_installed(PACKAGE_NAME), 'Package failed to install'

#!/usr/bin/env python2
"""
Reconfigures a Jenkins master running in Docker at container runtime.
"""

from __future__ import print_function

import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


def is_firstrun(jenkins_home_dir):
    """A small helper utility to determine if this is the first run of this
    bootstrap script. Checks to see if the 'jenkins_home_dir' directory
    is empty, or if it contains existing data.

    :param jenkins_home_dir: the path to $JENKINS_HOME on disk
    :return: boolean; True if $JENKINS_HOME isn't populated, false otherwise
    """
    return len(os.listdir(jenkins_home_dir)) == 0


def populate_jenkins_config_xml(config_xml, master, name, host, port, role, user):
    """Modifies a Jenkins master's 'config.xml' at runtime. Essentially, this
    replaces certain configuration options of the Mesos plugin, such as the
    framework name and the Jenkins URL that agents use to connect back to the
    master.

    :param config_xml: the path to Jenkins' 'config.xml' file
    :param name: the name of the framework, e.g. 'jenkins'
    :param host: the Mesos agent the task is running on
    :param port: the Mesos port the task is running on
    :param role: The role passed to the internal Jenkins configuration that denotes which resources can be launched
    :param user: the user the task is running on
    """
    tree, root = _get_xml_root(config_xml)
    mesos = root.find('./clouds/org.jenkinsci.plugins.mesos.MesosCloud')

    _find_and_set(mesos, './master', master)
    _find_and_set(mesos, './frameworkName', name)
    _find_and_set(mesos, './jenkinsURL', "http://{}:{}".format(host, port))
    _find_and_set(mesos, './role', role)
    _find_and_set(mesos, './slavesUser', user)
        
    tree.write(config_xml)


def populate_jenkins_location_config(location_xml, url):
    """Modifies a Jenkins master's location config at runtime. This
    replaces the value of 'jenkinsUrl' with url.

    :param location_xml: the path to Jenkins'
        'jenkins.model.JenkinsLocationConfiguration.xml' file
    :type location_xml: str
    :param url: the Jenkins instance URL
    :type url: str
    """
    tree, root = _get_xml_root(location_xml)
    _find_and_set(root, 'jenkinsUrl', url)
    tree.write(location_xml)


def populate_nginx_config(config_file, nginx_port, jenkins_port, context):
    """Modifies an nginx config, replacing the "magic" strings
    '_XNGINX_PORT', '_XJENKINS_PORT' and '_XJENKINS_CONTEXT' with the real
    value provided.

    :param config_file: the path to an 'nginx.conf'
    :param nginx_port: the Mesos port the task is running on
    :param jenkins_port: the Mesos port the task is running on
    :param context: the application's context, e.g. '/service/jenkins'
    """
    original = None
    with open(config_file, 'r') as f:
        original = f.readlines()

    with open(config_file, 'w') as f:
        for line in original:
            if re.match(r'.*_XNGINX_PORT.*', line):
                f.write(re.sub('_XNGINX_PORT', nginx_port, line))
            elif re.match(r'.*_XJENKINS_PORT.*', line):
                f.write(re.sub('_XJENKINS_PORT', jenkins_port, line))
            elif re.match(r'.*_XJENKINS_CONTEXT.*', line):
                f.write(re.sub('_XJENKINS_CONTEXT', context, line))
            else:
                f.write(line)


def populate_known_hosts(hosts, dest_file):
    """Gather SSH public key from one or more hosts and write out the
    known_hosts file.

    :param hosts: a string of hosts separated by whitespace
    :param dest_file: absolute path to the SSH known hosts file
    """
    dest_dir = os.path.dirname(dest_file)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    command = ['ssh-keyscan'] + hosts.split()
    subprocess.call(
        command, stdout=open(dest_file, 'w'), stderr=open(os.devnull, 'w'))


def main():
    try:
        jenkins_agent_user = os.environ['JENKINS_AGENT_USER']
        jenkins_agent_role = os.environ['JENKINS_AGENT_ROLE']
        jenkins_staging_dir = os.environ['JENKINS_STAGING']
        jenkins_home_dir = os.environ['JENKINS_HOME']
        jenkins_framework_name = os.environ['JENKINS_FRAMEWORK_NAME']
        jenkins_app_context = os.environ['JENKINS_CONTEXT']
        marathon_host = os.environ['HOST']
        marathon_nginx_port = os.environ['PORT0']
        marathon_jenkins_port = os.environ['PORT1']
        mesos_master = os.environ['JENKINS_MESOS_MASTER']
        ssh_known_hosts = os.environ['SSH_KNOWN_HOSTS']
    except KeyError:
        # Since each of the environment variables above are set either in the
        # DCOS marathon.json or by Marathon itself, the user should never get
        # to this point.
        print("ERROR: missing one or more required environment variables.")
        return 1

    # optional environment variables
    jenkins_root_url = os.getenv(
            'JENKINS_ROOT_URL',
            "http://{}:{}".format(marathon_host, marathon_nginx_port))


    # If this is the first run of the script, make changes to the staging
    # directory first, so we can then use these files to populate the host
    # volume. If data exists in that directory (e.g. Marathon has restarted
    # a Jenkins master task), then we'll make changes in-place to the existing
    # data without overwriting anything the user already has.
    firstrun = is_firstrun(jenkins_home_dir)
    jenkins_data_dir = jenkins_staging_dir if firstrun else jenkins_home_dir

    populate_jenkins_config_xml(
        os.path.join(jenkins_data_dir, 'config.xml'),
        mesos_master,
        jenkins_framework_name,
        marathon_host,
        marathon_nginx_port,
        jenkins_agent_role,
        jenkins_agent_user)

    populate_jenkins_location_config(os.path.join(
        jenkins_data_dir, 'jenkins.model.JenkinsLocationConfiguration.xml'),
        jenkins_root_url)

    populate_known_hosts(ssh_known_hosts, '/etc/ssh/ssh_known_hosts')

    # os.rename() doesn't work here because the destination directory is
    # actually a mount point to the volume on the host. shutil.move() here
    # also doesn't work because of some weird recursion problem.
    #
    # TODO(roger): figure out how to implement this in Python.
    #
    if firstrun:
        subprocess.call("/bin/mv {src}/* {dst}/.".format(
            src=jenkins_staging_dir, dst=jenkins_home_dir), shell=True)

    # nginx changes here are really "run once". The context should never
    # change as long as a Jenkins instance is alive, since the rewrite will
    # be based on the app ID in Marathon, as will the volume on disk.
    populate_nginx_config(
        '/etc/nginx/nginx.conf',
        marathon_nginx_port,
        marathon_jenkins_port,
        jenkins_app_context)


def _get_xml_root(config_xml):
    """Return the ET tree and root XML element.

    :param config_xml: path to config XML file
    :type config_xml: str
    :return: a tuple (tree,root)
    :rtype: tuple
    """
    tree = ET.parse(config_xml)
    root = tree.getroot()
    return tuple([tree, root])


def _find_and_set(element, term, new_text):
    """Find the desired term within the XML element and replace
    its text with text.

    :param element: XML element
    :type element: xml.etree.ElementTree.Element
    :param term: XML element to find
    :type term: str
    :param new_text: New element text
    :type new_text: str
    """
    element.find(term).text = new_text


if __name__ == '__main__':
    sys.exit(main())

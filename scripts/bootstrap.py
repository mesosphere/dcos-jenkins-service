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
    if len(os.listdir(jenkins_home_dir)) == 0:
        return True
    else:
        return False


def populate_jenkins_config_xml(config_xml, name, host, port):
    """Modifies a Jenkins master's 'config.xml' at runtime. Essentially, this
    replaces certain configuration options of the Mesos plugin, such as the
    framework name and the Jenkins URL that agents use to connect back to the
    master.

    :param config_xml: the path to Jenkins' 'config.xml' file
    :param name: the name of the framework, e.g. 'jenkins'
    :param host: the Mesos agent the task is running on
    :param port: the Mesos port the task is running on
    """
    tree = ET.parse(config_xml)
    root = tree.getroot()
    mesos = root.find('./clouds/org.jenkinsci.plugins.mesos.MesosCloud')

    mesos_frameworkName = mesos.find('./frameworkName')
    mesos_frameworkName.text = name

    mesos_jenkinsURL = mesos.find('./jenkinsURL')
    mesos_jenkinsURL.text = ''.join(['http://', host, ':', port])

    tree.write(config_xml)


def populate_jenkins_location_config(location_xml, host, port):
    """Modifies a Jenkins master's location config at runtime. Essentially,
    this replaces the value of 'jenkinsUrl' with a newly constructed URL
    based on the host and port that the Marathon app instance is running on.

    :param location_xml: the path to Jenkins'
        'jenkins.model.JenkinsLocationConfiguration.xml' file
    :param host: the Mesos agent the task is running on
    :param port: the Mesos port the task is running on
    """
    tree = ET.parse(location_xml)
    root = tree.getroot()
    jenkinsUrl = root.find('jenkinsUrl')
    jenkinsUrl.text = ''.join(['http://', host, ':', port])
    tree.write(location_xml)


def populate_tomcat_rewrite_config(config_file, context):
    """Modifies a Tomcat's 'rewrite.config', replacing the "magic" string
    '_XJENKINS_CONTEXT' with the real value provided by 'context'.

    :param config_file: the path to Tomcat's 'rewrite.config'
    :param context: the application's context, e.g. '/service/jenkins'
    """
    original = None
    with open(config_file, 'r') as f:
        original = f.readlines()

    with open(config_file, 'w') as f:
        for line in original:
            if re.match(r'.*_XJENKINS_CONTEXT.*', line):
                f.write(re.sub('_XJENKINS_CONTEXT', context, line))
            else:
                f.write(line)


def main():
    firstrun = True

    try:
        catalina_home = os.environ['CATALINA_HOME']
        jenkins_staging_dir = os.environ['JENKINS_STAGING']
        jenkins_home_dir = os.environ['JENKINS_HOME']
        jenkins_framework_name = os.environ['JENKINS_FRAMEWORK_NAME']
        jenkins_app_context = os.environ['JENKINS_CONTEXT']
        marathon_host = os.environ['HOST']
        marathon_port = os.environ['PORT0']
    except KeyError:
        # Since each of the environment variables above are set either in the
        # DCOS marathon.json or by Marathon itself, the user should never get
        # to this point.
        print("ERROR: missing one or more required environment variables.")
        return 1

    # If this is the first run of the script, make changes to the staging
    # directory first, so we can then use these files to populate the host
    # volume. If data exists in that directory (e.g. Marathon has restarted
    # a Jenkins master task), then we'll make changes in-place to the existing
    # data without overwriting anything the user already has.
    if is_firstrun(jenkins_home_dir):
        jenkins_data_dir = jenkins_staging_dir
    else:
        firstrun = False
        jenkins_data_dir = jenkins_home_dir

    populate_jenkins_config_xml(os.path.join(
        jenkins_data_dir, 'config.xml'),
        jenkins_framework_name, marathon_host, marathon_port)

    populate_jenkins_location_config(os.path.join(
        jenkins_data_dir, 'jenkins.model.JenkinsLocationConfiguration.xml'),
        marathon_host, marathon_port)

    # os.rename() doesn't work here because the destination directory is
    # actually a mount point to the volume on the host. shutil.move() here
    # also doesn't work because of some weird recursion problem.
    #
    # TODO(roger): figure out how to implement this in Python.
    #
    if firstrun:
        subprocess.call("/bin/mv {src}/* {dst}/.".format(
            src=jenkins_staging_dir, dst=jenkins_home_dir), shell=True)

    # Tomcat changes here are really "run once". The context should never
    # change as long as a Jenkins instance is alive, since the context will
    # be based on the app ID in Marathon, as will the volume on disk.
    populate_tomcat_rewrite_config(os.path.join(
        catalina_home, 'conf', 'Catalina', 'localhost', 'rewrite.config'),
        jenkins_app_context)


if __name__ == '__main__':
    sys.exit(main())

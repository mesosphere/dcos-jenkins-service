# Jenkins on DC/OS
[![Build Status](https://jenkins.mesosphere.com/service/jenkins/buildStatus/icon?job=Jenkins/public-jenkins-dcos-master)](https://jenkins.mesosphere.com/service/jenkins/view/Velocity/job/Jenkins/job/public-jenkins-dcos-master/)
[![Docker Stars](https://img.shields.io/docker/stars/mesosphere/jenkins.svg)][docker-hub]
[![Docker Pulls](https://img.shields.io/docker/pulls/mesosphere/jenkins.svg)][docker-hub]
[![](https://images.microbadger.com/badges/image/mesosphere/jenkins.svg)](http://microbadger.com/images/mesosphere/jenkins "Get your own image badge on microbadger.com")

Run a Jenkins master on DC/OS, using Docker and Nginx. This Jenkins instance is pre-configured to autoscale build agents onto the DC/OS cluster using the [Jenkins Mesos plugin][mesos-plugin].

## Overview
This repo contains a [Dockerfile](Dockerfile) that runs Jenkins inside a Docker
container and uses [Nginx][nginx-home] as a reverse proxy. It also provides
several Jenkins plugins and a basic Jenkins configuration in order to get you
up and running quickly with Jenkins on DC/OS.

## Reporting issues

Please report issues and submit feature requests for Jenkins on DC/OS by [creating an issue in the DC/OS JIRA][dcos-jira] (JIRA account required).

## Included in this repo
Base packages:
  * [Jenkins][jenkins-home] 2.107.2 (LTS)
  * [Nginx][nginx-home] 1.10.1

Jenkins plugins:
  * ant v1.8
  * ansicolor v0.5.2
  * antisamy-markup-formatter v1.5
  * artifactory v2.15.1
  * authentication-tokens v1.3
  * azure-credentials v1.6.0
  * azure-vm-agents v0.7.0
  * blueocean v1.5.0
  * branch-api v2.0.19
  * build-name-setter v1.6.9
  * build-timeout v1.19
  * cloudbees-folder v6.4
  * conditional-buildstep v1.3.6
  * config-file-provider v2.16.4
  * copyartifact v1.39.1
  * cvs v2.14
  * docker-build-publish v1.3.2
  * docker-workflow v1.15.1
  * durable-task v1.22
  * ec2 v1.39
  * embeddable-build-status v1.9
  * external-monitor-job v1.7
  * ghprb v1.40.0
  * git v3.8.0
  * git-client v2.7.1
  * git-server v1.7
  * github v1.29.0
  * github-api v1.90
  * github-branch-source v2.3.3
  * github-organization-folder v1.6
  * gitlab-plugin v1.5.5
  * gradle v1.28
  * greenballs v1.15
  * handlebars v1.1.1
  * ivy v1.28
  * jackson2-api v2.8.11.1
  * job-dsl v1.68
  * jobConfigHistory v2.18
  * jquery v1.12.4-0
  * ldap v1.20
  * mapdb-api v1.0.9.0
  * marathon v1.6.0
  * matrix-auth v2.2
  * matrix-project v1.13
  * maven-plugin v3.1.2
  * mesos v0.16
  * metrics v3.1.2.11
  * momentjs v1.1.1
  * monitoring v1.70.0
  * nant v1.4.3
  * node-iterator-api v1.5.0
  * pam-auth v1.3
  * parameterized-trigger v2.35.2
  * pipeline-build-step v2.7
  * pipeline-github-lib v1.0
  * pipeline-input-step v2.8
  * pipeline-milestone-step v1.3.1
  * pipeline-model-api:1.2.8
  * pipeline-model-definition v1.2.8
  * pipeline-model-extensions v1.2.5
  * pipeline-rest-api v2.10
  * pipeline-stage-step v2.3
  * pipeline-stage-view v2.10
  * plain-credentials v1.4
  * rebuild v1.28
  * role-strategy v2.7.0
  * run-condition v1.0
  * s3 v0.11.0
  * saferestart v0.3
  * saml v1.0.5
  * scm-api v2.2.6
  * ssh-agent v1.15
  * ssh-slaves v1.26
  * subversion v2.10.5
  * timestamper v1.8.9
  * translation v1.16
  * variant v1.1
  * windows-slaves v1.3.1
  * workflow-aggregator v2.5
  * workflow-api v2.26
  * workflow-basic-steps v2.6
  * workflow-cps v2.47
  * workflow-cps-global-lib v2.9
  * workflow-durable-task-step v2.19
  * workflow-job v2.17
  * workflow-multibranch v2.17
  * workflow-scm-step v2.6
  * workflow-step-api v2.14
  * workflow-support v2.18

## Packaging
Jenkins is available as a package in the [Mesosphere Universe][universe].
To make changes to the Jenkins package, submit a pull request against the
Universe.

## Installation

To install Jenkins for the DC/OS, simply run `dcos package install jenkins` or install via the Universe page in the DC/OS UI.

Jenkins should now be available at <http://dcos.example.com/service/jenkins>.
See [Getting Started][getting-started] for more in-depth instructions and
configuration options.

## Releasing
To release a new version of this package:

  1. Update [the Jenkins conf][jenkins-conf] to reference the current release of
  the [jenkins-dind][jenkins-dind] Docker image (if needed).
  2. Add some release notes to [CHANGELOG.md](CHANGELOG.md)
  3. Tag the commit on master that you want to be released.
  4. Once [the build][jenkins-build] has successfully completed, submit a new
  pull request against [the Universe][universe] referencing the new tag.

[dcos-jira]: https://jira.mesosphere.com/secure/CreateIssueDetails!init.jspa?pid=14110&issuetype=3
[docker-hub]: https://hub.docker.com/r/mesosphere/jenkins
[getting-started]: https://docs.mesosphere.com/service-docs/jenkins/quickstart/
[jenkins-conf]: /conf/jenkins/config.xml
[jenkins-dind]: https://github.com/mesosphere/jenkins-dind-agent
[jenkins-home]: https://jenkins-ci.org/
[mesos-plugin]: https://github.com/jenkinsci/mesos-plugin
[nginx-home]: http://nginx.org/en/
[jenkins-build]: https://jenkins.mesosphere.com/service/jenkins/job/public-jenkins-dcos-master/
[universe]: https://github.com/mesosphere/universe

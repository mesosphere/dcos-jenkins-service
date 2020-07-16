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
  * [Jenkins][jenkins-home] 2.190.1 (LTS)
  * [Nginx][nginx-home] 1.10.1

Jenkins plugins: see [plugins.conf](plugins.conf).

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

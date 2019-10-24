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

Jenkins plugins:
  * ace-editor v1.1
  * ansicolor v0.6.2
  * ant v1.10
  * antisamy-markup-formatter v1.6
  * apache-httpcomponents-client-4-api v4.5.10-1.0
  * artifactory v3.4.1
  * authentication-tokens v1.3
  * aws-credentials v1.28
  * aws-java-sdk v1.11.636
  * azure-commons v1.0.4
  * azure-credentials v1.6.1
  * azure-vm-agents v1.2.2
  * blueocean v1.19.0
  * bouncycastle-api v2.17
  * branch-api v2.5.4
  * build-name-setter v2.0.3
  * build-timeout v1.19
  * cloudbees-bitbucket-branch-source v2.5.0
  * cloudbees-folder v6.9
  * cloud-stats v0.25
  * command-launcher v1.3
  * conditional-buildstep v1.3.6
  * config-file-provider v3.6.2
  * configuration-as-code v1.31
  * copyartifact v1.42.1
  * credentials v2.3.0
  * credentials-binding v1.20
  * cvs v2.14
  * display-url-api v2.3.2
  * docker-build-publish v1.3.2
  * docker-commons v1.15
  * docker-workflow v1.19
  * durable-task v1.30
  * ec2 v1.46.1
  * embeddable-build-status v2.0.2
  * external-monitor-job v1.7
  * favorite v2.3.2
  * git v3.12.1
  * git-client v2.8.6
  * github v1.29.4
  * github-api v1.95
  * github-branch-source v2.5.8
  * github-organization-folder v1.6
  * gitlab-plugin v1.5.13
  * git-server v1.8
  * gradle v1.34
  * greenballs v1.15
  * handlebars v1.1.1
  * handy-uri-templates-2-api v2.1.7-1.0
  * htmlpublisher v1.21
  * ivy v2.1
  * jackson2-api v2.9.10
  * javadoc v1.5
  * jdk-tool v1.3
  * jenkins-design-language v1.19.0
  * jira v3.0.10
  * jobConfigHistory v2.24
  * job-dsl v1.76
  * jquery v1.12.4-1
  * jquery-detached v1.2.1
  * jquery-ui v1.0.2
  * jsch v0.1.55.1
  * junit v1.28
  * ldap v1.20
  * lockable-resources v2.5
  * mailer v1.29
  * mapdb-api v1.0.9.0
  * marathon v1.6.0
  * matrix-auth v2.4.2
  * matrix-project v1.14
  * maven-plugin v3.4
  * mercurial v2.8
  * mesos v1.0.0
  * metrics v4.0.2.6
  * momentjs v1.1.1
  * monitoring v1.79.0
  * nant v1.4.3
  * node-iterator-api v1.5.0
  * pam-auth v1.5.1
  * parameterized-trigger v2.35.2
  * pipeline-build-step v2.9
  * pipeline-github-lib v1.0
  * pipeline-graph-analysis v1.10
  * pipeline-input-step v2.11
  * pipeline-milestone-step v1.3.1
  * pipeline-model-api v1.3.9
  * pipeline-model-declarative-agent v1.1.1
  * pipeline-model-definition v1.3.9
  * pipeline-model-extensions v1.3.9
  * pipeline-rest-api v2.12
  * pipeline-stage-step v2.3
  * pipeline-stage-tags-metadata v1.3.9
  * pipeline-stage-view v2.12
  * plain-credentials v1.5
  * prometheus v2.0.6
  * pubsub-light v1.13
  * rebuild v1.31
  * role-strategy v2.14
  * run-condition v1.2
  * s3 v0.11.2
  * saferestart v0.3
  * saml v1.1.3
  * scm-api v2.6.3
  * script-security v1.66
  * sse-gateway v1.20
  * ssh-agent v1.17
  * ssh-credentials v1.17.3
  * ssh-slaves v1.30.2
  * structs v1.20
  * subversion v2.12.2
  * timestamper v1.10
  * token-macro v2.8
  * translation v1.16
  * trilead-api v1.0.5
  * variant v1.3
  * windows-slaves v1.4
  * workflow-aggregator v2.6
  * workflow-api v2.37
  * workflow-basic-steps v2.18
  * workflow-cps v2.74
  * workflow-cps-global-lib v2.15
  * workflow-durable-task-step v2.34
  * workflow-job v2.35
  * workflow-multibranch v2.21
  * workflow-scm-step v2.9
  * workflow-step-api v2.20
  * workflow-support v3.3

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

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
  * [Jenkins][jenkins-home] 2.164.2 (LTS)
  * [Nginx][nginx-home] 1.10.3

Jenkins plugins:
  * ace-editor:1.1
  * ansicolor:0.5.2
  * ant:1.8
  * antisamy-markup-formatter:1.5
  * apache-httpcomponents-client-4-api:4.5.5-3.0
  * artifactory:2.16.2
  * authentication-tokens:1.3
  * aws-credentials:1.26
  * aws-java-sdk:1.11.457
  * azure-commons:0.2.11
  * azure-credentials:1.6.0
  * azure-vm-agents:0.7.3
  * blueocean-autofavorite:1.2.4
  * blueocean-bitbucket-pipeline:1.14.0
  * blueocean-commons:1.14.0
  * blueocean-config:1.14.0
  * blueocean-core-js:1.14.0
  * blueocean-dashboard:1.14.0
  * blueocean-display-url:2.2.0
  * blueocean-events:1.14.0
  * blueocean-executor-info:1.14.0
  * blueocean-git-pipeline:1.14.0
  * blueocean-github-pipeline:1.14.0
  * blueocean-i18n:1.14.0
  * blueocean-jira:1.14.0
  * blueocean-jwt:1.14.0
  * blueocean-personalization:1.14.0
  * blueocean-pipeline-api-impl:1.14.0
  * blueocean-pipeline-editor:1.14.0
  * blueocean-pipeline-scm-api:1.14.0
  * blueocean-rest-impl:1.14.0
  * blueocean-rest:1.14.0
  * blueocean-web:1.14.0
  * blueocean:1.14.0
  * bouncycastle-api:2.17
  * branch-api:2.0.20
  * build-name-setter:1.6.9
  * build-timeout:1.19
  * cloud-stats:0.23
  * cloudbees-bitbucket-branch-source:2.4.4
  * cloudbees-folder:6.5.1
  * conditional-buildstep:1.3.6
  * config-file-provider:2.18
  * copyartifact:1.39.1
  * credentials-binding:1.18
  * credentials:2.1.18
  * cvs:2.14
  * display-url-api:2.3.1
  * docker-build-publish:1.3.2
  * docker-commons:1.14
  * docker-workflow:1.17
  * durable-task:1.25
  * ec2:1.39
  * embeddable-build-status:1.9
  * external-monitor-job:1.7
  * favorite:2.3.2
  * ghprb:1.42.0
  * git-client:2.7.3
  * git-server:1.7
  * git:3.9.1
  * github-api:1.92
  * github-branch-source:2.3.6
  * github-organization-folder:1.6
  * github:1.29.2
  * gitlab-plugin:1.5.9
  * gradle:1.29
  * greenballs:1.15
  * handlebars:1.1.1
  * handy-uri-templates-2-api:2.1.7-1.0
  * htmlpublisher:1.18
  * ivy:1.28
  * jackson2-api:2.8.11.3
  * javadoc:1.5
  * jenkins-design-language:1.14.0
  * jira:3.0.6
  * job-dsl:1.70
  * jobConfigHistory:2.19
  * jquery-detached:1.2.1
  * jquery:1.12.4-0
  * jsch:0.1.55
  * junit:1.27
  * ldap:1.20
  * mailer:1.23
  * mapdb-api:1.0.9.0
  * marathon:1.6.0
  * matrix-auth:2.3
  * matrix-project:1.13
  * maven-plugin:3.1.2
  * mercurial:2.6
  * metrics:3.1.2.11
  * momentjs:1.1.1
  * monitoring:1.73.1
  * nant:1.4.3
  * node-iterator-api:1.5.0
  * pam-auth:1.4
  * parameterized-trigger:2.35.2
  * pipeline-build-step:2.7
  * pipeline-github-lib:1.0
  * pipeline-graph-analysis:1.9
  * pipeline-input-step:2.8
  * pipeline-milestone-step:1.3.1
  * pipeline-model-api:1.3.2
  * pipeline-model-declarative-agent:1.1.1
  * pipeline-model-definition:1.3.2
  * pipeline-model-extensions:1.3.2
  * pipeline-rest-api:2.10
  * pipeline-stage-step:2.3
  * pipeline-stage-tags-metadata:1.3.8
  * pipeline-stage-view:2.10
  * plain-credentials:1.4
  * pubsub-light:1.12
  * rebuild:1.28
  * role-strategy:2.9.0
  * run-condition:1.2
  * s3:0.11.2
  * saferestart:0.3
  * saml:1.0.7
  * scm-api:2.2.7
  * script-security:1.57
  * sse-gateway:1.17
  * ssh-agent:1.16
  * ssh-credentials:1.15
  * ssh-slaves:1.28
  * structs:1.17
  * subversion:2.11.1
  * timestamper:1.8.10
  * token-macro:2.7
  * translation:1.16
  * variant:1.1
  * workflow-aggregator:2.5
  * workflow-api:2.30
  * workflow-basic-steps:2.8.2
  * workflow-cps-global-lib:2.11
  * workflow-cps:2.55
  * workflow-durable-task-step:2.21
  * workflow-job:2.25
  * workflow-multibranch:2.20
  * workflow-scm-step:2.6
  * workflow-step-api:2.16
  * workflow-support:2.20

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

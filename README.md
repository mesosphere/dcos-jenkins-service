# Jenkins on DC/OS
[![Build Status](https://jenkins.mesosphere.com/service/jenkins/buildStatus/icon?job=Jenkins/public-jenkins-dcos-master)](https://jenkins.mesosphere.com/service/jenkins/view/Velocity/job/Jenkins/job/public-jenkins-dcos-master/)
[![Docker Stars](https://img.shields.io/docker/stars/mesosphere/jenkins.svg)][docker-hub]
[![Docker Pulls](https://img.shields.io/docker/pulls/mesosphere/jenkins.svg)][docker-hub]
[![](https://images.microbadger.com/badges/image/mesosphere/jenkins.svg)](http://microbadger.com/images/mesosphere/jenkins "Get your own image badge on microbadger.com")

Run a Jenkins master on Mesos and Marathon, using Docker and Nginx.

## Overview
This repo contains a [Dockerfile](Dockerfile) that runs Jenkins inside a Docker
container and uses [Nginx][nginx-home] as a reverse proxy. It also provides
several Jenkins plugins and a basic Jenkins configuration in order to get you
up and running quickly with Jenkins on DC/OS.

## Included in this repo
Base packages:
  * [Jenkins][jenkins-home] 2.19.1 (LTS)
  * [Nginx][nginx-home] 1.10.1

Jenkins plugins:
  * ace-editor v1.1
  * ansicolor v0.4.2
  * ant v1.4
  * antisamy-markup-formatter v1.5
  * artifactory v2.7.2
  * async-http-client v1.7.24.1
  * authentication-tokens v1.3
  * aws-credentials v1.16
  * aws-java-sdk v1.11.37
  * azure-slave-plugin v0.3.3
  * blueocean v1.0.0-b09
  * blueocean-commons v1.0.0-b09
  * blueocean-config v1.0.0-b09
  * blueocean-dashboard v1.0.0-b09
  * blueocean-events v1.0.0-b09
  * blueocean-jwt v1.0.0-b09
  * blueocean-personalization v1.0.0-b09
  * blueocean-pipeline-api-impl v1.0.0-b09
  * blueocean-rest v1.0.0-b09
  * blueocean-rest-impl v1.0.0-b09
  * blueocean-web v1.0.0-b09
  * bouncycastle-api v2.16.0
  * branch-api v1.11
  * build-name-setter v1.6.5
  * build-timeout v1.17.1
  * cloudbees-folder v5.13
  * conditional-buildstep v1.3.5
  * config-file-provider v2.13
  * copyartifact v1.38.1
  * credentials v2.1.7
  * credentials-binding v1.9
  * cvs v2.12
  * display-url v0.5
  * docker-commons v1.5
  * durable-task v1.12
  * ec2 v1.36
  * embeddable-build-status v1.9
  * external-monitor-job v1.6
  * favorite v1.16
  * ghprb v1.33.1
  * git v2.6.0
  * git-client v1.21.0
  * git-server v1.7
  * github v1.22.3
  * github-api v1.77
  * github-branch-source v1.10
  * gitlab v1.4.2
  * gradle v1.25
  * greenballs v1.15
  * handlebars v1.1.1
  * icon-shim v2.0.3
  * ivy v1.26
  * jackson2-api v2.7.3
  * javadoc v1.4
  * job-dsl v1.52
  * jobConfigHistory v2.15
  * jquery v1.11.2-0
  * jquery-detached v1.2.1
  * junit v1.19
  * ldap v1.13
  * mailer v1.18
  * mapdb-api v1.0.9.0
  * marathon v1.3.2
  * matrix-auth v1.4
  * matrix-project v1.7.1
  * maven-plugin v2.14
  * mesos v0.13.1
  * metrics v3.1.2.9
  * momentjs v1.1.1
  * monitoring v1.62.0
  * nant v1.4.3
  * node-iterator-api v1.5.0
  * pam-auth v1.3
  * parameterized-trigger v2.32
  * pipeline-build-step v2.3
  * pipeline-graph-analysis v1.2
  * pipeline-input-step v2.3
  * pipeline-milestone-step v1.1
  * pipeline-model-definition v0.4
  * pipeline-rest-api v2.1
  * pipeline-stage-step v2.2
  * pipeline-stage-view v2.1
  * plain-credentials v1.3
  * rebuild v1.25
  * role-strategy v2.3.2
  * run-condition v1.0
  * s3 v0.10.10
  * saferestart v0.3
  * saml v0.12
  * scm-api v1.3
  * script-security v1.24
  * sse-gateway v1.10
  * ssh-agent v1.13
  * ssh-credentials v1.12
  * ssh-slaves v1.11
  * structs v1.5
  * subversion v2.7.1
  * support-core v2.33
  * timestamper v1.8.7
  * token-macro v2.0
  * translation v1.15
  * variant v1.0
  * windows-slaves v1.2
  * workflow-aggregator v2.4
  * workflow-api v2.5
  * workflow-basic-steps v2.2
  * workflow-cps v2.21
  * workflow-cps-global-lib v2.4
  * workflow-docker v1.9
  * workflow-durable-task-step v2.5
  * workflow-job v2.7
  * workflow-multibranch v2.9
  * workflow-scm-step v2.2
  * workflow-step-api v2.4
  * workflow-support v2.10


## Creating the WAR
The included `pom.xml` file is used to create a WAR file containing the plugins
listed above. To assemble the WAR file, run the [maven][apache-maven] command:
`mvn package`.

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
  2. Update the Jenkins release version in [pom.xml](pom.xml).
  3. Add some release notes to [CHANGELOG.md](CHANGELOG.md)
  4. Tag the commit on master that you want to be released.
  5. Once [the build][jenkins-build] has successfully completed, submit a new
  pull request against [the Universe][universe] referencing the new tag.

[apache-maven]: https://maven.apache.org
[docker-hub]: https://hub.docker.com/r/mesosphere/jenkins
[getting-started]: http://mesosphere.github.io/jenkins-dcos/docs/
[jenkins-conf]: /conf/jenkins/config.xml
[jenkins-dind]: https://github.com/mesosphere/jenkins-dind-agent
[jenkins-home]: https://jenkins-ci.org/
[nginx-home]: http://nginx.org/en/
[jenkins-build]: https://jenkins.mesosphere.com/service/jenkins/job/public-jenkins-dcos-master/
[universe]: https://github.com/mesosphere/universe

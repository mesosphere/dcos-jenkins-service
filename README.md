# Jenkins on Mesos
[![velocity](http://velocity.mesosphere.com/service/velocity/buildStatus/icon?job=public-jenkins-mesos-master)](http://velocity.mesosphere.com/service/velocity/job/public-jenkins-mesos-master/)
[![Docker Stars](https://img.shields.io/docker/stars/mesosphere/jenkins.svg)][docker-hub]
[![Docker Pulls](https://img.shields.io/docker/pulls/mesosphere/jenkins.svg)][docker-hub]
[![Image Size](https://img.shields.io/imagelayers/image-size/mesosphere/jenkins/0.2.3.svg)](https://imagelayers.io/?images=mesosphere/jenkins:0.2.3)
[![Image Layers](https://img.shields.io/imagelayers/layers/mesosphere/jenkins/0.2.3.svg)](https://imagelayers.io/?images=mesosphere/jenkins:0.2.3)

Run a Jenkins master on Mesos and Marathon, using Docker and Nginx.

## Overview
This repo contains a [Dockerfile](Dockerfile) that runs Jenkins inside a Docker
container and uses [Nginx][nginx-home] as a reverse proxy. It also provides
several Jenkins plugins and a basic Jenkins configuration in order to get you
up and running quickly with Jenkins on DCOS.

## Included in this repo
Base packages:
  * [Jenkins][jenkins-home] 1.651.1 (LTS)
  * [Nginx][nginx-home] 1.9.9

Jenkins plugins:
  * [ansicolor][ansicolor-plugin] v0.4.2
  * [artifactory][artifactory-plugin] v2.4.7
  * [build-name-setter][build-name-setter-plugin] v1.6.3
  * [build-pipeline][build-pipeline-plugin] v1.5.2
  * [build-timeout][build-timeout-plugin] v1.16
  * [cloudbees-folder][folders-plugin] v5.7
  * [credentials][credentials-plugin] v1.26
  * [credentials-binding][credentials-binding-plugin] v1.7
  * [embeddable-build-status][embeddable-build-status-plugin] v1.9
  * [ghprb][ghprb-plugin] v1.31.3
  * [git][git-plugin] v2.4.4
  * [git-client][git-client-plugin] v1.19.6
  * [github][github-plugin] v1.18.1
  * [github-api][github-api-plugin] v1.72.1
  * [greenballs][greenballs-plugin] v1.15
  * [job-dsl][job-dsl-plugin] v1.44
  * [jobConfigHistory][jobConfigHistory-plugin] v2.13
  * [jquery][jquery] v1.11.2-0
  * [mailer][mailer-plugin] v1.16
  * [marathon][marathon-plugin] v1.1
  * [mesos][mesos-plugin] v0.12.0
  * [monitoring][monitoring-plugin] v1.59.0
  * [parameterized-trigger][parameterized-trigger-plugin] v2.30
  * [plain-credentials][plain-credentials] v1.1
  * [rebuild][rebuild-plugin] v1.25
  * [role-strategy][role-strategy-plugin] v2.2.0
  * [saferestart][saferestart-plugin] v0.3
  * [saml][saml-plugin] v0.5
  * [scm-api][scm-api-plugin] v0.2
  * [script-security][script-security-plugin] v1.17
  * [ssh-credentials][ssh-credentials-plugin] v1.11
  * [timestamper][timestamper-plugin] v1.7.4
  * [token-macro][token-macro-plugin] v1.12.1
  * [workflow-step-api][workflow-step-api] v1.15

## Creating the WAR
The included `pom.xml` file is used to create a WAR file containing the plugins
listed above. To assemble the WAR file, run the [maven][apache-maven] command:
`mvn package`.

## Packaging
Jenkins is available as a package in the [Mesosphere Universe][universe].
To make changes to the Jenkins package, submit a pull request against the
Universe.

## Installation
To install Jenkins for the DCOS, perform the following steps.

  1. Run `dcos package update`
  2. Run `dcos package install jenkins`

Jenkins should now be available at <http://dcos.example.com/service/jenkins>.
See [Getting Started][getting-started] for more in-depth instructions and
configuration options.

## Releasing
To release a new version of this package:

  1. Update [the Jenkins conf][jenkins-conf] to reference the current release of
  the [jenkins-dind][jenkins-dind] Docker image (if needed).
  2. Tag the commit on master that you want to be released.
  3. Once [the build][jenkins-build] has successfully completed, submit a new
  pull request against [the Universe][universe] referencing the new tag.


[apache-maven]: https://maven.apache.org
[ansicolor-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/AnsiColor+Plugin
[artifactory-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Artifactory+Plugin
[build-name-setter-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Build+Name+Setter+Plugin
[build-pipeline-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin
[build-timeout-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Build-timeout+Plugin
[credentials-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Credentials+Plugin
[credentials-binding-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Credentials+Binding+Plugin
[docker-hub]: https://hub.docker.com/r/mesosphere/jenkins
[embeddable-build-status-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Embeddable+Build+Status+Plugin
[folders-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/CloudBees+Folders+Plugin
[getting-started]: http://mesosphere.github.io/jenkins-mesos/docs/
[ghprb-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/GitHub+pull+request+builder+plugin
[git-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin
[git-client-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Git+Client+Plugin
[github-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/GitHub+Plugin
[github-api-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/GitHub+API+Plugin
[greenballs-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Green+Balls
[jenkins-conf]: /conf/jenkins/config.xml
[jenkins-dind]: https://github.com/mesosphere/jenkins-dind-agent
[jenkins-home]: https://jenkins-ci.org/
[job-dsl-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Job+DSL+Plugin
[jobConfigHistory-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/JobConfigHistory+Plugin
[jquery]: https://wiki.jenkins-ci.org/display/JENKINS/jQuery+Plugin
[mailer-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Mailer
[marathon-plugin]: https://github.com/mesosphere/jenkins-marathon-plugin
[mesos-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Mesos+Plugin
[monitoring-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Monitoring
[nginx-home]: http://nginx.org/en/
[parameterized-trigger-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Parameterized+Trigger+Plugin
[plain-credentials]: https://wiki.jenkins-ci.org/display/JENKINS/Plain+Credentials+Plugin
[rebuild-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Rebuild+Plugin
[role-strategy-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Role+Strategy+Plugin
[saferestart-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/SafeRestart+Plugin
[saml-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/SAML+Plugin
[scm-api-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/SCM+API+Plugin
[script-security-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Script+Security+Plugin
[ssh-credentials-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/SSH+Credentials+Plugin
[jenkins-build]: https://velocity.mesosphere.com/service/velocity/job/public-jenkins-mesos-master/
[timestamper-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Timestamper
[token-macro-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Token+Macro+Plugin
[universe]: https://github.com/mesosphere/universe
[workflow-step-api]: https://wiki.jenkins-ci.org/display/JENKINS/Pipeline+Plugin

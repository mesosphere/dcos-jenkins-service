# Jenkins on Mesos [![Build Status](https://teamcity.mesosphere.io/guestAuth/app/rest/builds/buildType:(id:Oss_Jenkins_PublishDevelopmentDocker)/statusIcon)](https://teamcity.mesosphere.io/viewType.html?buildTypeId=Oss_Jenkins_PublishDevelopmentDocker&guest=1)
Run a Jenkins master on Mesos and Marathon, using Docker and Nginx.

## Overview
This repo contains a [Dockerfile](Dockerfile) that runs Jenkins inside a Docker
container and uses [Nginx][nginx-home] as a reverse proxy. It also provides
several Jenkins plugins and a basic Jenkins configuration in order to get you
up and running quickly with Jenkins on DCOS.

## Included in this repo
Base packages:
  * [Jenkins][jenkins-home] 1.642.1 (LTS)
  * [Nginx][nginx-home] 1.9.9

Jenkins plugins:
  * [ansicolor][ansicolor-plugin] v0.4.2
  * [credentials][credentials-plugin] v1.24
  * [git][git-plugin] v2.4.1
  * [git-client][git-client-plugin] v1.19.2
  * [greenballs][greenballs-plugin] v1.15
  * [job-dsl][job-dsl-plugin] v1.42
  * [jobConfigHistory][jobConfigHistory-plugin] v2.12
  * [mesos][mesos-plugin] v0.9.0
  * [monitoring][monitoring-plugin] v1.58.0
  * [parameterized-trigger][parameterized-trigger-plugin] v2.30
  * [rebuild][rebuild-plugin] v1.25
  * [saferestart][saferestart-plugin] v0.3
  * [scm-api][scm-api-plugin] v0.2
  * [script-security][script-security-plugin] v1.17
  * [ssh-credentials][ssh-credentials-plugin] v1.11
  * [token-macro][token-macro-plugin] v1.12.1

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

  1. Update [the Jenkins conf][jenkins-conf] to reference the next release of
  the [jenkins-dind][jenkins-dind] Docker image.
  2. Tag the commit on master that you want to be released.
  3. Once [the build][teamcity-build] has successfully completed, submit a new
  pull request against [the Universe][universe] referencing the new tag.


[ansicolor-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/AnsiColor+Plugin
[credentials-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Credentials+Plugin
[getting-started]: http://mesosphere.github.io/jenkins-mesos/docs/
[git-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin
[git-client-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Git+Client+Plugin
[greenballs-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Green+Balls
[jenkins-conf]: /conf/jenkins/config.xml
[jenkins-dind]: /dind-agent/README.md
[jenkins-home]: https://jenkins-ci.org/
[job-dsl-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Job+DSL+Plugin
[jobConfigHistory-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/JobConfigHistory+Plugin
[mesos-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Mesos+Plugin
[monitoring-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Monitoring
[nginx-home]: http://nginx.org/en/
[parameterized-trigger-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Parameterized+Trigger+Plugin
[rebuild-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Rebuild+Plugin
[saferestart-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/SafeRestart+Plugin
[scm-api-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/SCM+API+Plugin
[script-security-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Script+Security+Plugin
[ssh-credentials-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/SSH+Credentials+Plugin
[teamcity-build]: https://teamcity.mesosphere.io/viewType.html?buildTypeId=Oss_Jenkins_PublishReleaseDocker
[token-macro-plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Token+Macro+Plugin
[universe]: https://github.com/mesosphere/universe

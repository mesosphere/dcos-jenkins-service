# Changes

## v2.0.0-2.7.2 (2016-08-11)
  * Includes Jenkins 2.7.2 LTS and re-bundles common plugins. Note that the new
  "Getting Started" wizard has been disabled for this package
  * Includes the new "Pipeline" set of plugins
  * Includes the new Blue Ocean UI (currently in Alpha) as an optional UI
  * Added AWS and Azure plugins for on-demand cloud VMs, for when containers
  might not work for a specific build
  * Added the Support plugin, for easily generating support bundles
  * Added the Metrics plugin
  * Bumped all previously installed plugins to their latest versions
  * Removed the Build Pipeline plugin, since it has been superseded by the
  newer, shinier Pipeline plugin


## v1.0.0-1.651.3 (2016-07-19)
  * Includes the [Marathon plugin][marathon-plugin].
  * Allow Jenkins instance URL to be configurable
  * Add several plugins, including Artifactory, Role Strategy, SAML,
  Embeddable Build Status, GitHub Pull Request Builder, etc.
  * Update various plugins to latest versions
  * Update Jenkins core to latest LTS release
  * Bundle plugins with the Jenkins war itself, instead of being
  loaded by `plugin_install.sh`.
  * Upgraded plugins affected by SECURITY-170.

## v0.2.3 (2016-03-17)
  * Separate Jenkins dind-agent into a standalone project:
  https://github.com/mesosphere/jenkins-dind-agent
  * Add github-api plugin, which is a dependency for the github plugin
  * Add acceptance tests

## v0.2.2 (2016-03-10)
  * DinD image now uses the `overlay` storage driver instead of `vfs`, which
  results in a (roughly) 10x performance and storage improvement. This was
  tested on both CoreOS and CentOS 7.1 with the default Docker configuration.
  * Update Mesos plugin to v0.11.0
  * Add GitHub plugin
  * Misc fixes and documentation updates

## v0.2.1 (2016-02-28)
  * Jenkins agents created by the Mesos plugins will no longer attempt to
  reconnect when they fail to connect to the master
  * Update Mesos plugin version to 0.10.0
  * Add the credentials binding plugin, and several dependencies
  * Add the build pipeline plugin
  * Add the jQuery plugin
  * Update DinD base image to 1.10
  * Update JRE 7 to JDK 8 in the dind-agent image, and add the ca-certificates
  package
  * Install perl in the dind-agent image, which is required for some Git
  operations
  * Documentation updates and other misc fixes

## v0.2.0 (2016-02-05)
  * Update Jenkins to 1.642.1
  * Update various plugins to the latest versions
  * Add jobConfigHistory plugin to Jenkins
  * Check for plugin updates when building the Docker image
  * Support for third-party Git servers (populating the SSH known hosts file)
  * Maintain the Mesos master URL in bootstrap.py
  * Swap Tomcat for Nginx to improve URL rewriting when accessing Jenkins
  through Admin Router
  * Rewrote Git history, removing old binaries over 1M, to improve future
  development experience
  * Other misc fixes

## v0.1.5 (2016-01-19)
  * Add a Jenkins Docker-in-Docker (dind) agent image to the repo, for building
    Docker containers when running on top of DCOS.

## v0.1.4 (2016-01-19)
  * Remove the labelString configuration entirely
  * Remove a mention of the Mesosphere Multiverse repo in the docs

## v0.1.3 (2016-01-11)
  * Update Jenkins to 1.625.3
  * Update the Jenkins Mesos plugin to v0.9.0
  * Update the Tomcat version to v8.0.30
  * Add the ansicolor plugin to Jenkins
  * Switch to the `java:openjdk-8-jdk` image, which includes build dependencies
    such as Git
  * Use ZooKeeper for Mesos master resolution
  * Update the included Jenkins agent label expression

## v0.1.2 (2015-12-02)
  * Connect to `leader.mesos` instead of `master.mesos` in HA deployments

## v0.1.1 (2015-11-17)
  * Include Jenkins 1.625.2, which includes security updates
  * Add some basic docs

## v0.1.0 (2015-10-22)
Initial release

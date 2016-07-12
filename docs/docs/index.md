---
title: Setting Up and Running Jenkins
---

## Setting Up and Running Jenkins

### Quickstart

Jenkins on DC/OS works by running the Jenkins master as a one-instance Marathon
application. Once the Jenkins master comes online, it registers itself as
a Mesos framework (using the [jenkins-mesos][jenkins-mesos-plugin] plugin).

This project aims to make it easy to run Jenkins as a DC/OS service, as
described on the [Overview](../) page.

### Requirements

<div class="alert alert-warning" role="alert">
<strong>Note:</strong> Jenkins on DC/OS is only supported in version 1.4 and
later. If you aren't yet running DC/OS 1.4 and would like to try out Jenkins,
please contact <a href="mailto:support@mesosphere.io">support@mesosphere.io</a>.
</div>

* A running DC/OS cluster, version 1.4 or later
* A single NFS (or other network storage / distributed filesystem) share
mounted at the same path on every node (e.g. `/mnt/nfs`)

### Installation and Configuration

To install the Jenkins package for DC/OS, perform the following steps.

  1. Create an `options.json` file with site-specific information, such as
  the path to the NFS share on the host. For a complete example, please see
  the [Configuration Reference](configuration.html).
  2. Run `dcos package update`
  3. Run `dcos package install jenkins --options=options.json`

Jenkins will now be available at <http://dcos-master/service/jenkins>.

### Uninstalling

To uninstall Jenkins, you will need to remove the application as a DC/OS
service. Note that you will need to manually clean-up any job configurations
and/or build data that may have been stored on your NFS share.

Using the DC/OS CLI, simply run `dcos package uninstall jenkins`.

[jenkins-mesos-plugin]: https://github.com/jenkinsci/mesos-plugin
[dcos-cli-home]: https://github.com/dcos/dcos-cli

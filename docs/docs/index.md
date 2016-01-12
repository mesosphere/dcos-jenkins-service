---
title: Setting Up and Running Jenkins
---

## Setting Up and Running Jenkins

### Quickstart

Jenkins on Mesos works by running the Jenkins master as a one-instance Marathon
application. Once the Jenkins master comes online, it registers itself as
a Mesos framework (using the [jenkins-mesos][jenkins-mesos-plugin] plugin).

This project aims to make it easy to run Jenkins as a Marathon service, both
on open source Marathon and on the Mesosphere DCOS, as described on the
[Overview](../) page.

### Requirements

<div class="alert alert-warning" role="alert">
<strong>Note:</strong> Jenkins on DCOS is only supported in version 1.4 and
later. If you aren't yet running DCOS 1.4 and would like to try out Jenkins,
please contact <a href="mailto:support@mesosphere.io">support@mesosphere.io</a>.
</div>

* A running Mesosphere DCOS cluster, version 1.4 or later
  * Alternately, you can be running an open source Mesos cluster plus
  Mesosphere's Marathon framework. For more information, please refer to
  [Marathon's Docker documentation][marathon-native-docker-docs].
* A single NFS (or other network storage / distributed filesystem) share
mounted at the same path on every node (e.g. `/mnt/nfs`)

### Installation and Configuration

#### Mesosphere DCOS

To install the Jenkins service for the Mesosphere DCOS, perform the following
steps.

  1. Create an `options.json` file with site-specific information, such as
  the path to the NFS share on the host. For a complete example, please see
  the [Configuration Reference](configuration.html).
  2. Run `dcos package update`
  3. Run `dcos package install jenkins --options=options.json`

Jenkins will now be available at <http://dcos-master/service/jenkins>.

#### Marathon Open Source

The easiest way to deploy the application on Marathon is using the open source
[DCOS CLI][dcos-cli-home]. But first, you'll need to set a few options for
the tool to connect to your open source Mesos and Marathon instances.

Assuming the Mesos master is running on port 5050, and Marathon is running
on port 8080 (the defaults), run the following commands.

```
$ dcos config set core.mesos_master_url http://<mesos-master>:5050
$ dcos config set marathon.url http://<marathon-host>:8080
```

### Uninstalling

To uninstall Jenkins, you will need to remove the application as a DCOS
service, or destroy the application from your Marathon instance. Note that
you will need to manually clean-up any job configurations and/or build data
that may have been stored on your NFS share.

#### Mesosphere DCOS

Using the DCOS CLI, simply run `dcos package uninstall jenkins`.

#### Marathon Open Source

Assuming the application ID is `jenkins`, run the following command.

```
$ curl -X DELETE http://marathon-host/v2/apps/jenkins
```

[jenkins-mesos-plugin]: https://github.com/jenkinsci/mesos-plugin
[marathon-native-docker-docs]: https://mesosphere.github.io/marathon/docs/native-docker.html
[dcos-cli-home]: https://github.com/mesosphere/dcos-cli

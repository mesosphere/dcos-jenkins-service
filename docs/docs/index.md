---
title: Setting Up and Running Jenkins
---

## {{page.title}}

### Quickstart

Jenkins on Mesos works by running the Jenkins master as a one-instance Marathon
application. Once the Jenkins master comes online, it registers itself as
a Mesos framework (using the [jenkins-mesos][jenkins-mesos-plugin] plugin).

This project aims to make it easy to run Jenkins as a Marathon service, both
on open source Marathon and on the Mesosphere DCOS, as described on the
[Overview](../) page.

### Requirements

* A running Mesosphere DCOS cluster
  * Alternately, you can be running an open source Mesos cluster plus
  Mesosphere's Marathon framework. If you're running Mesos open source, please
  be sure that Docker Engine is configured and running on each of the agents,
  and that the Mesos agent has been configured to use the Docker
  containerizer.
* A single NFS (or other network storage / distributed filesystem) share
mounted at the same path on every node (e.g. `/mnt/nfs`)

### Installation and Configuration

#### Mesosphere DCOS

To install the Jenkins service for the Mesosphere DCOS, perform the following
steps.

  1. Create an `options.json` file with site-specific information, such as
  the path to the NFS share on the host. For a complete example, please see
  the [Configuration Reference](configuration.html).
  2. [Add the Mesosphere Multiverse repo to your DCOS CLI][dcos-multiverse].
  3. Run `dcos package update`
  4. Run `dcos package install jenkins --options=options.json`

Jenkins will now be available at <http://the-dcos-master/service/jenkins>.

#### Marathon Open Source

To install the Jenkins service using Marathon Open Source, you'll need to
create a JSON file containing the Marathon application definition. For an
example of what this might look like, see the
[Configuration Reference](configuration.html).

Assuming you have that file on-disk as `marathon-jenkins.json`, run the
following command.

```
$ curl -H 'Content-Type: application/json' -d @marathon-jenkins.json http://marathon-host/v2/apps
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
[dcos-multiverse]: https://github.com/mesosphere/multiverse/#instructions

---
title: Overview
---

<div class="jumbotron text-center">
  <h1>Jenkins</h1>
  <p class="lead">
    Jenkins on Mesos is the most resource efficient way to do CI in your datacenter.
  </p>
  <p>
    <a href="https://github.com/mesosphere/jenkins-mesos"
        class="btn btn-lg btn-primary">
      Jenkins repository
    </a>
  </p>
</div>

## Overview

Jenkins on Mesos from Mesosphere is the best way to efficiently run a CI
infrastructure in your datacenter. By deploying Jenkins masters via
[Marathon][marathon-home] or [DCOS][dcos-home], Jenkins will run builds based
on available compute resources as offered by an underlying
[Apache Mesos][mesos-home] cluster.

Up to this point, there have been two main issues with running Jenkins masters
on Marathon:

  1. persisting job configurations and build data across instance restarts or
  node failures
  2. the instance running on an unpredictable host and/or port within the
  cluster
  3. Jenkins uses absolute URLs (e.g. `/jenkins/foo/bar.baz` instead of
  `foo/bar.baz`), which makes providing a reverse proxy for the service in
  DCOS a bit complicated

We've attempted to solve each of these problems with this project:

  1. until persistent volumes are supported in Mesos and DCOS, we require the
  user has a mount point at the same location on each of their Mesos or DCOS
  nodes (e.g. `/mnt/nfs`) so that data can be shared across nodes in the
  infrastructure. This could be accomplished using NFS, an iSCSI
  target, or really any other file storage service or distributed filesystem.
  2. we've included a bootstrap script that makes targeted configuration
  changes to Jenkins at container runtime. This includes the values of the
  Jenkins "root URL", as well as the `jenkinsURL` value specific to the
  jenkins-mesos plugin. It won't modify any other configuration, so the user
  is able to customize their Jenkins installation to their liking
  3. we run `jenkins.war` within the [Apache Tomcat][tomcat-home] application
  server, so that we have greater control over URL re-writing inside the
  container

For an up-to-date list of the software bundled with this project, please see
the [README][jenkins-mesos-readme-master] file located within the GitHub
repository.

[marathon-home]: http://mesosphere.github.io/marathon/
[dcos-home]: https://mesosphere.com/product/
[mesos-home]: http://mesos.apache.org/
[tomcat-home]: http://tomcat.apache.org/
[jenkins-mesos-readme-master]: https://github.com/mesosphere/jenkins-mesos/blob/master/README.md

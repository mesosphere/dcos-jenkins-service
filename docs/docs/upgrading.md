---
title: Upgrade Notes
---

# Upgrade Notes

## Upgrade Procedure

To upgrade from one version of the Jenkins on DC/OS package to another, simply uninstall the current versions, update your package repository cache and install a new version.

1. Uninstall Jenkins as per the instructions on [Getting Started]({{ site.baseurl }}/docs/). Any builds that are current in progress or queued will be lost.

2. Update your local cache of the package repository: `dcos package update`.

3. Install Jenkins, again following the instructions on [Getting Started]({{ site.baseurl }}/docs/). Make sure you use the same configuration file as previously, specifically pointing Jenkins to the same `host-volume`.

4. Currently it is necessary to upgrade plugins by hand using the Jenkins UI at `<dcos_url>/service/jenkins/pluginManager`. In the future, it will be possible to do this through the DC/OS package configuration.

## Upgrading to 0.1.3

### Label String Configuration Changes

Prior to this release, it was necessary to select "Restrict where this project can be run" and set the "Label Expression" to "mesos". This was because the Jenkins Mesos plugin would only run builds that matched a "Label String", which we configured to be "mesos".

In this release, we upgraded the Jenkins Mesos plugin from version 0.8.0 to version 0.9.0 which allows you to leave "Label String" blank. This means you no longer need to set this for each build.

If you have previously installed Jenkins, the package will re-use your existing configuration. If you wish to remove this limitation, simply go to "Manage Jenkins" > "Configure System" and clicked on the "Advanced" button under "Mesos Cloud". Then, delete the contents of the "Label String" textbox.

![Label String Illustration]({{site.baseurl}}/img/label-string.png)

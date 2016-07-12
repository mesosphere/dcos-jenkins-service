---
title: Configuring Builds
---

# Configuring Builds

DC/OS runs everything inside Docker by default. This is to minimise dependencies
on the underlying host operating system and to allow for maximum resilience in
the case of a host failing.

When using Jenkins on DC/OS, the Mesos scheduler creates new Jenkins slaves that
run as Mesos tasks within a Docker container. Builds that the user configures
are then run inside the same container. Since many builds typically involve
steps that invoke the Docker utility, e.g. `docker build` or `docker push`, we
provide a `mesosphere/jenkins-dind` Docker image and configure the Mesos plugin
to use this by default.

This image includes many tools by default
([Dockerfile](https://github.com/mesosphere/jenkins-dcos/blob/master/dind-agent/Dockerfile)):

    * OpenJDK 7
    * Python 2
    * Python 3
    * Bash
    * Git
    * ssh

However, in many cases, you will have your own dependencies to specify for your
build. You can do these by providing unique container images for each type of
build. The instructions below specify how you can do this.

# Creating Custom Agent Containers

The recommended approach to providing your own dependencies is to extend the
provided `jenkins-dind-agent` image and install the packages you require.

The example below shows how you could create an image which includes `sbt`, a
Scala build tool (the following code snippet is based on
[docker-sbt](https://github.com/1science/docker-sbt/blob/latest/Dockerfile)):

```sh
FROM mesosphere/jenkins-dind:0.2.0

ENV SBT_VERSION 0.13.8
ENV SBT_HOME /usr/local/sbt
ENV PATH ${PATH}:${SBT_HOME}/bin

RUN curl -sL "http://dl.bintray.com/sbt/native-packages/sbt/$SBT_VERSION/sbt-$SBT_VERSION.tgz" | gunzip | tar -x -C /usr/local && \
    echo -ne "- with sbt $SBT_VERSION\n" >> /root/.built
```

## Configuring SSH Host Keys (optional)

If you aren't using GitHub to host your git repositories and wish to use ssh to
clone your git repositories, you will need to add your git server's host keys
to `/etc/ssh/ssh_known_hosts`. 

Adding the following lines to your Dockerfile will add your keys, replacing
`my.git.server` with the actual hostname:

```sh
ENV SSH_KNOWN_HOSTS github.com my.git.server
RUN ssh-keyscan $SSH_KNOWN_HOSTS | tee /etc/ssh/ssh_known_hosts
```

This is necessary because strict host key checking is on by default and clones
over ssh will fail if your host keys aren't explicitly added.

## Pushing

Once built, you can then push this to DockerHub or your own private Docker
registry. This registry must be accessible by DC/OS agents.

## Configuring Jenkins

To make this image available to builds in Jenkins, you need to add it manually
via the "Manage Jenkins" -> "Configure Jenkins" page.

Scroll to the "Cloud" section at the bottom and press "Advanced". You will see
a grey button to "Add Slave Info":

![Add Slave Info]({{site.baseurl}}/img/add-slave-info.png)

Most of the defaults are sufficient here but you may wish to change the "Label
String" to something that reflects the contents of this custom build file. In
this case, we'll set the label string to `sbt`:

![sbt Label String]({{site.baseurl}}/img/sbt-label-string.png)

To set up the new image, press "Advanced" again and select the "Use Docker
Containerizer" checkbox. Here you can specify the Docker Image name. Be sure to
select "Docker Privileged Mode" and to specify a custom Docker command shell of
`wrapper.sh`:

![Docker Containerizer Settings]({{site.baseurl}}/img/docker-containerizer-settings.png)

Don't forget to hit Save!

## Configuring Your Build

Finally, to configure a build to use the newly specified image, click on
"Configure" for the build, select "Restrict where this project can be run" and
specify the same "Label String":

![Build Label String Configuration]({{site.baseurl}}/img/build-label-string.png)

Again, don't forget to hit "Save"!

# Jenkins Demo
The demo job and script in this directory will create a pre-configured number
of jobs on a Jenkins master, randomizing their duration and final build result.
This serves to demonstrate the functionality of the [Mesos plugin][mesos-plugin]
for Jenkins, which allows build agents to be launched on demand using containers
on a Mesos cluster.

After a preconfigured duration of inactivity, each of the containers will be
destroyed by the Mesos plugin, freeing the resources to be consumed by other
Mesos frameworks.

## Usage
Provision a [Mesosphere DCOS][mesosphere-dcos] cluster and install Jenkins:

```
$ dcos package install --yes jenkins
```

Launch the demo script, passing in the cluster URL:

```
$ ./demo.sh create http://dcos.cluster.url/service/jenkins
```

Navigate to the Jenkins instance to observe the Mesos plugin in action:

```
$ open http://dcos.cluster.url/service/jenkins
```

If you'd like to cleanup the Jenkins instance, so that you can re-run the demo,
run the script with the `cleanup` command:

```
$ ./demo.sh cleanup http://dcos.cluster.url/service/jenkins
```

[mesos-plugin]: https://github.com/jenkinsci/mesos-plugin
[mesosphere-dcos]: https://mesosphere.com/product/

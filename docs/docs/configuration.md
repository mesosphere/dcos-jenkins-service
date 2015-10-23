---
title: Configuration
---

# Configuration

## Mesosphere DCOS

To configure Jenkins on Mesos for the Mesosphere DCOS, create a new file called
`options.json` in your working directory. This file will contain options
specific to your environment, such as the name of the framework (e.g.
`jenkins-test`, `jenkins-release`, etc), and the path to the NFS share you want
to save your Jenkins configuration and build data to.

The following example will create a new DCOS service named `jenkins-myteam` and
use the NFS share located at `/mnt/nfs/jenkins_data`:

```
{
    "jenkins": {
        "framework-name": "jenkins-myteam",
        "host_volume": "/mnt/nfs/jenkins_data"
    }
}
```

*Tip: the value of `host_volume` is the base path to a share on a NFS server
or other distributed filesystem. The actual path on-disk for this particular
example will be `/mnt/nfs/jenkins_data/jenkins-myteam`.*

Assuming your DCOS service options have been saved to the file `options.json`,
you can install Jenkins with your site-specific configuration by running
the following command.

```
$ dcos package install jenkins --options=options.json
```

Wait a few moments for the instance to become healthy, then access the
`jenkins-myteam` service via the DCOS UI.

## Marathon Open Source

The Marathon application definition will be very similar to the DCOS service
configuration. The service configuration can currently be found in the
[Mesosphere Multiverse][mesosphere-multiverse] repository.

Here's one example of what your Marathon application might look like.

```
{
  "id": "jenkins-1",
  "cpus": 1.0,
  "mem": 768.0,
  "instances": 1,
  "env": {
      "CATALINA_OPTS": "-Xms512m -Xmx512m -Dport.http=$PORT0 -Dcontext.path=$JENKINS_CONTEXT",
      "JENKINS_FRAMEWORK_NAME": "jenkins-1",
      "JENKINS_CONTEXT": "/jenkins-1",
      "LD_LIBRARY_PATH": "/opt/mesosphere/lib"
  },
   "container": {
       "type": "DOCKER",
       "docker": {
           "image": "mesosphere/jenkins:0.1.0",
           "network": "HOST"
       },
       "volumes": [
           {
               "containerPath": "/var/jenkins_home",
               "hostPath": "/mnt/nfs/jenkins_data/jenkins-1",
               "mode": "RW"
           },
           {
               "containerPath": "/opt/mesosphere/lib",
               "hostPath": "/usr/lib",
               "mode": "RO"
           }
       ]
   },
   "healthChecks": [
    {
      "path": "/jenkins-1"
      "portIndex": 0,
      "protocol": "HTTP",
      "gracePeriodSeconds": 30,
      "intervalSeconds": 60,
      "timeoutSeconds": 20,
      "maxConsecutiveFailures": 3
    }
  ]
}
```

[mesosphere-multiverse]: https://github.com/mesosphere/multiverse

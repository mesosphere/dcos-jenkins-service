---
title: Configuration
---

# Configuration

To configure Jenkins for DC/OS, create a new file called `options.json` in your
working directory. This file will contain options specific to your environment,
such as the name of the framework (e.g.  `jenkins-test`, `jenkins-release`,
etc), and the path to the NFS share you want to save your Jenkins configuration
and build data to.

The following example will create a new DC/OS service named `jenkins-myteam` and
use the NFS share located at `/mnt/nfs/jenkins_data`:

```json
{
    "jenkins": {
        "framework-name": "jenkins-myteam",
        "host-volume": "/mnt/nfs/jenkins_data"
    }
}
```

*Tip: the value of `host-volume` is the base path to a share on a NFS server
or other distributed filesystem. The actual path on-disk for this particular
example will be `/mnt/nfs/jenkins_data/jenkins-myteam`.*

#### Pinning to a Host

If you like, you can also specify a `pinned-hostname` constraint. This is
useful if you don't have NFS available and need to pin Jenkins to a specific
node:

```json
{
    "jenkins": {
        "framework-name": "jenkins-pinned",
        "host-volume": "/var/jenkins_data",
        "pinned-hostname": "10.0.0.100"
    }
}
```

#### Known Hosts

The option `known-hosts` allows you to specify a space-separated list of
hostnames that you'd like to retrieve the SSH public keys for. This list will
be populated on the Jenkins master when the bootstrap script is run (at
container launch time). Note that you will need to manually ensure that the
SSH known hosts list is populated in any Jenkins agent containers; an example
is included in the `dind-image` directory located at the root of this repo.

```json
{
    "jenkins": {
        "framework-name": "jenkins-private-git",
        "host-volume": "/mnt/nfs/jenkins_data",
        "known-hosts": "github.com git.apache.org git.example.com"
    }
}
```

### Installation

Assuming your DC/OS service options have been saved to the file `options.json`,
you can install Jenkins with your site-specific configuration by running
the following command.

```
$ dcos package install jenkins --options=options.json
```

Wait a few moments for the instance to become healthy, then access the
`jenkins-myteam` service via the DC/OS UI.

[dcos-cli-home]: https://github.com/dcos/dcos-cli

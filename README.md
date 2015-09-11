Jenkins on Mesos
================

Jenkins standalone instance package with the Mesos plugin pre-installed


# Universe Package

Jenkins is available as a package in the [Mesosphere Multiverse](https://github.com/mesosphere/multiverse/). To make changes to the Jenkins package, submit a pull-request against the Multiverse.

## Installation

1) Ensure [the Multiverse repo has been added](https://github.com/mesosphere/multiverse/#instructions) to your DCOS CLI.

2) `dcos package update`

3) `dcos package install jenkins`


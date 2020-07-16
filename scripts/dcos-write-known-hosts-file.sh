#!/bin/bash

# This script writes out the SSH known hosts file which has the hosts sourced from
# the SSH_KNOWN_HOSTS env-var which is in-turn specified via the service config settings.

arg=$SSH_KNOWN_HOSTS
lstrip_space=${arg#' '}
rstrip_space=${lstrip_space%' '}
SSH_KEYSCAN_ARGS=$rstrip_space

SSH_KNOWN_HOSTS_DIR="$JENKINS_HOME/.ssh/"
SSH_KNOWN_HOSTS_FILE="$JENKINS_HOME/.ssh/ssh_known_hosts"

# Create the directory if it doesn't exist.
mkdir -p $SSH_KNOWN_HOSTS_DIR

ssh-keyscan  $SSH_KEYSCAN_ARGS > $SSH_KNOWN_HOSTS_FILE

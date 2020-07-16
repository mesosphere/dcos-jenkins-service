#!/bin/bash

#This script will produce valid DNS scheme to be used for Mesos DNS resolution.

#Strip out leading and trailing slashes.
arg=$JENKINS_FRAMEWORK_NAME
lstrip_slash=${arg#'/'}
rstrip_slash=${lstrip_slash%'/'}

#Tokenize path
IFS='/' read -r -a tokenize <<< "$rstrip_slash"

#Reverse the path to conform with DNS lookups.
FRAMEWORK_DNS_NAME=""

min=0
max=$(( ${#tokenize[@]} -1 ))
while [[ max -ge min ]]
do
    # Note the '-' at the end we will strip out later.
    FRAMEWORK_DNS_NAME+="${tokenize[$max]}-"   
    (( max-- ))
done

#Strip out trailing '-' from earlier.
JENKINS_FRAMEWORK_NAME=${FRAMEWORK_DNS_NAME%'-'}

#Export out for consumption.
export JENKINS_FRAMEWORK_NAME

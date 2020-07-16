#!/bin/bash

# This script enables multi-tenancy features available from DC/OS 2.0 and later. 
# This script forces $JENKINS_AGENT_ROLE to match $MESOS_ALLOCATION_ROLE
# Only when $MARATHON_APP_ENFORCE_GROUP_ROLE is set.

IS_ENFORCE_GROUP_ROLE=""
_str2bool() {
    local test_condition=${1,,}
    case $test_condition in
        "yes" | "true" | "t" | "y" | "1")
            IS_ENFORCE_GROUP_ROLE="True"
        ;;
        "no" | "false" | "f" | "n" | "0")
            IS_ENFORCE_GROUP_ROLE=""
        ;;
        *)
            IS_ENFORCE_GROUP_ROLE=""
   esac
}

if [ -z "$MESOS_ALLOCATION_ROLE" ] || [ -z "$MARATHON_APP_ENFORCE_GROUP_ROLE" ]; then
    echo "INFO: This cluster does not have multi-tenant features. Using legacy non-quota enforcement aware semantics."
    exit 0
fi

#Filter all variants of true here.
_str2bool $MARATHON_APP_ENFORCE_GROUP_ROLE

if [ ! -z "$IS_ENFORCE_GROUP_ROLE" ]; then
    if [ "$MESOS_ALLOCATION_ROLE" != "$JENKINS_AGENT_ROLE" ]; then
        echo "WARN: JENKINS_AGENT_ROLE:'$JENKINS_AGENT_ROLE' not the same as MESOS_ALLOCATION_ROLE:'$MESOS_ALLOCATION_ROLE'." 
        echo "enforceRole detected on top-level group, using '$MESOS_ALLOCATION_ROLE' as agent-role." 
    fi 
    JENKINS_AGENT_ROLE=$MESOS_ALLOCATION_ROLE 
    export $JENKINS_AGENT_ROLE
    echo "INFO: using enforced group role '$JENKINS_AGENT_ROLE' for agents."
else
    echo "INFO: using non-enforced group role '$JENKINS_AGENT_ROLE' for agents."
fi

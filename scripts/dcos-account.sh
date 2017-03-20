#!/bin/sh 
#
# Write DC/OS credentials to file and update environment
# variables accordingly.
#

# check if the SSL file exists and if not assume it needs
# the MESOS_SANDBOX prefix.
write_cred_file()
{
    if [ -n "$DCOS_SERVICE_ACCOUNT_CREDENTIAL" ] && [ "$DCOS_SERVICE_ACCOUNT_CREDENTIAL" != file* ]; then
        local target_file="$JENKINS_HOME/.dcos_acct_creds"
        echo "$DCOS_SERVICE_ACCOUNT_CREDENTIAL" > $target_file

        # fix env variable
        DCOS_SERVICE_ACCOUNT_CREDENTIAL="file://$target_file"
        export DCOS_SERVICE_ACCOUNT_CREDENTIAL
    fi
}


write_cred_file

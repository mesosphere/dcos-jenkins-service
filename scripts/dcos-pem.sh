#!/bin/sh
#
# Write DC/OS PEM from ENV variable to file and update environment
# variables accordingly.
#

# Check if DCOS_PEM is present in env variables
# and if so write content to local disk. This will overwrite the env 
# variable with the file location and import the PEM into the JVM keystore.
write_pem_file()
{
    if [ -n "$DCOS_PEM" ]; then
        local target_file="$JENKINS_HOME/.dcos_pem_64"
        printf "%s" "$DCOS_PEM" > $target_file
        #printf "Found DCOS_PEM environment variable, writing for import to $target_file"

        local decoded_target_file="$JENKINS_HOME/.dcos_pem"
        /usr/bin/openssl base64 -d -in $target_file -out $decoded_target_file 

        # fix env variable
        DCOS_PEM="file://$target_file"
        export DCOS_PEM

        # update the JVM keystore with the PEM
        ${JAVA_HOME}/bin/keytool -keystore ${JAVA_HOME}/jre/lib/security/cacerts -import -alias dcos -file $decoded_target_file -storepass changeit -noprompt
    fi
}

write_pem_file

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
    # DC/OS specific. 
    if [ -f "$LIBPROCESS_SSL_CA_FILE" ]; then
        echo "Adding $LIBPROCESS_SSL_CA_FILE to JVM keystore..."
        local target_file="$JENKINS_HOME/.dcos_pem"
        cat $LIBPROCESS_SSL_CA_FILE | openssl x509 -outform PEM > $target_file

        # fix env variable
        DCOS_PEM="file://$target_file"
        export DCOS_PEM

        # update the JVM keystore with the PEM
        ${JAVA_HOME}/bin/keytool -keystore ${JAVA_HOME}/jre/lib/security/cacerts -import -alias dcos -file $target_file -storepass changeit -noprompt
    else
        echo "Skipping cert import, file $LIBPROCESS_SSL_CA_FILE not found. This is ok if this container is not run on DC/OS..."
    fi
}

write_pem_file

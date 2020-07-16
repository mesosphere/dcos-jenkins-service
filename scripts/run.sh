#!/bin/bash

if [[ ! -z "$JENKINS_OPT_ADDITIONAL_PLUGINS" ]]; then
    echo "Installing additional plugins..."
    export REF=/var/jenkins_home
    export JENKINS_WAR=${JENKINS_FOLDER}/jenkins.war
    CURL_OPTIONS="-fkL" /usr/local/bin/install-plugins.sh $JENKINS_OPT_ADDITIONAL_PLUGINS 2>&1
    echo "Completed installing additional plugins..."
else
    echo "No additional plugins requested for installation..."
fi

#Run setup scripts.
. /usr/local/jenkins/bin/export-libssl.sh
. /usr/local/jenkins/bin/dcos-account.sh
. /usr/local/jenkins/bin/dcos-quota.sh
. /usr/local/jenkins/bin/dcos-framework-dns-name.sh
. /usr/local/jenkins/bin/dcos-write-known-hosts-file.sh

# Set Nginx parameters
envsubst '\$PORT0 \$PORT1 \$JENKINS_CONTEXT' < /var/nginx/nginx.conf.template > /var/nginx/nginx.conf

# Remove any previous jenkins-mesos-plugin builds directly injected into the build path.
# This was done in versions 3.5.4-2.150.1 and prior, this practice is now deprecated.
rm -f  /var/jenkins_home/plugins/mesos.hpi

nginx -c /var/nginx/nginx.conf    \
  && java ${JVM_OPTS}                                \
     -Duser.home="${MESOS_SANDBOX}"                  \
     -Dhudson.model.DirectoryBrowserSupport.CSP="${JENKINS_CSP_OPTS}" \
     -Dhudson.udp=-1                                 \
     -Djava.awt.headless=true                        \
     -Dhudson.DNSMultiCast.disabled=true             \
     -Djenkins.install.runSetupWizard=false          \
     -Djenkins.model.Jenkins.slaveAgentPort=${PORT2} \
     -Djenkins.model.Jenkins.slaveAgentPortEnforce=true \
     -jar ${JENKINS_FOLDER}/jenkins.war              \
     ${JENKINS_OPTS}                                 \
     --httpPort=${PORT1}                             \
     --webroot=${JENKINS_FOLDER}/war                 \
     --ajp13Port=-1                                  \
     --httpListenAddress=127.0.0.1                   \
     --ajp13ListenAddress=127.0.0.1                  \
     --prefix=${JENKINS_CONTEXT}

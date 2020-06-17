#!/bin/bash

export LD_LIBRARY_PATH=/libmesos-bundle/lib:/libmesos-bundle/lib/mesos:$LD_LIBRARY_PATH
export MESOS_NATIVE_JAVA_LIBRARY=$(ls /libmesos-bundle/lib/libmesos-*.so)

. /usr/local/jenkins/bin/export-libssl.sh

/usr/local/jenkins/bin/bootstrap.py
. /usr/local/jenkins/bin/dcos-account.sh

# Remove any previous jenkins-mesos-plugin builds directly injected into the build path.
# This was done in versions 3.5.4-2.150.1 and prior, this practice is now deprecated.
rm -f  /var/jenkins_home/plugins/mesos.hpi

nginx -c /var/nginx/nginx.conf    \
  && java ${JVM_OPTS}                                \
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

#!/bin/bash

export LD_LIBRARY_PATH=/libmesos-bundle/lib:/libmesos-bundle/lib/mesos:$LD_LIBRARY_PATH
export JENKINS_SLAVE_AGENT_PORT=$PORT_AGENT
export MESOS_NATIVE_JAVA_LIBRARY=$(ls /libmesos-bundle/lib/libmesos-*.so)

. /usr/local/jenkins/bin/export-libssl.sh

/usr/local/jenkins/bin/bootstrap.py
. /usr/local/jenkins/bin/dcos-account.sh

nginx -c /var/nginx/nginx.conf    \
  && java ${JVM_OPTS}                                \
     -Dhudson.model.DirectoryBrowserSupport.CSP="${JENKINS_CSP_OPTS}" \
     -Dhudson.udp=-1                                 \
     -Djava.awt.headless=true                        \
     -Dhudson.DNSMultiCast.disabled=true             \
     -Djenkins.install.runSetupWizard=false          \
     -Djavamelody.statsd-address="${STATSD_UDP_HOST}:${STATSD_UDP_PORT}"  \
     -jar ${JENKINS_FOLDER}/jenkins.war              \
     ${JENKINS_OPTS}                                 \
     --httpPort=${PORT1}                             \
     --webroot=${JENKINS_FOLDER}/war                 \
     --ajp13Port=-1                                  \
     --httpListenAddress=127.0.0.1                   \
     --ajp13ListenAddress=127.0.0.1                  \
     --prefix=${JENKINS_CONTEXT}

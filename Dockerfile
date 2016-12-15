FROM nginx:1.10.1
WORKDIR /tmp

# Environment variables used throughout this Dockerfile
#
# $JENKINS_STAGING  will be used to download plugins and copy config files
#                   during the Docker build process.
#
# $JENKINS_HOME     will be the final destination that Jenkins will use as its
#                   data directory. This cannot be populated before Marathon
#                   has a chance to create the host-container volume mapping.
#
ENV JENKINS_STAGING /var/jenkins_staging
ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_FOLDER /usr/share/jenkins/
ENV JAVA_HOME "/usr/lib/jvm/java-7-openjdk-amd64"

RUN apt-get update
RUN apt-get install -y git python zip curl default-jre jq gradle ant maven

RUN mkdir -p /var/log/nginx/jenkins
COPY conf/nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p $JENKINS_HOME
RUN mkdir -p ${JENKINS_FOLDER}/war

COPY target/jenkins-*.war ${JENKINS_FOLDER}/jenkins.war
COPY scripts/bootstrap.py /usr/local/jenkins/bin/bootstrap.py
COPY scripts/export-libssl.sh /usr/local/jenkins/bin/export-libssl.sh

COPY conf/jenkins/config.xml "${JENKINS_STAGING}/config.xml"
COPY conf/jenkins/jenkins.model.JenkinsLocationConfiguration.xml "${JENKINS_STAGING}/jenkins.model.JenkinsLocationConfiguration.xml"
COPY conf/jenkins/nodeMonitors.xml "${JENKINS_STAGING}/nodeMonitors.xml"

# Override the default property for DNS lookup caching
RUN echo 'networkaddress.cache.ttl=60' >> ${JAVA_HOME}/jre/lib/security/java.security

CMD . /usr/local/jenkins/bin/export-libssl.sh && \
	/usr/local/jenkins/bin/bootstrap.py && nginx && \
java ${JVM_OPTS}                                    \
    -Dhudson.udp=-1                                 \
    -Djava.awt.headless=true                        \
    -Dhudson.DNSMultiCast.disabled=true             \
    -Djenkins.install.runSetupWizard=false          \
    -jar ${JENKINS_FOLDER}/jenkins.war              \
    ${JENKINS_OPTS}                                 \
    --httpPort=${PORT1}                             \
    --webroot=${JENKINS_FOLDER}/war                 \
    --ajp13Port=-1                                  \
    --httpListenAddress=127.0.0.1                   \
    --ajp13ListenAddress=127.0.0.1                  \
    --prefix=${JENKINS_CONTEXT}

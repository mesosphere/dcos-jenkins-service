FROM tomcat:8.0.30-jre8
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
# $CATALINA_HOME    is derived from the official Tomcat Dockerfile:
#                   https://github.com/docker-library/tomcat/blob/df283818c1/8-jre8/Dockerfile
#
ENV JENKINS_WAR_URL https://updates.jenkins-ci.org/download/war/1.625.3/jenkins.war
ENV JENKINS_STAGING /var/jenkins_staging
ENV JENKINS_HOME /var/jenkins_home
ENV CATALINA_HOME /usr/local/tomcat
ENV PATH "${CATALINA_HOME}/bin:${PATH}"
ENV JAVA_HOME "/usr/lib/jvm/java-8-openjdk-amd64"


RUN rm -rf "${CATALINA_HOME}/webapps/*"
RUN mkdir -p $JENKINS_HOME

ADD $JENKINS_WAR_URL "${CATALINA_HOME}/webapps/"

COPY scripts/plugin_install.sh /usr/local/jenkins/bin/plugin_install.sh
COPY scripts/bootstrap.py /usr/local/jenkins/bin/bootstrap.py

COPY conf/jenkins/config.xml "${JENKINS_STAGING}/config.xml"
COPY conf/jenkins/jenkins.model.JenkinsLocationConfiguration.xml "${JENKINS_STAGING}/jenkins.model.JenkinsLocationConfiguration.xml"
COPY conf/jenkins/nodeMonitors.xml "${JENKINS_STAGING}/nodeMonitors.xml"
COPY conf/tomcat/server.xml "${CATALINA_HOME}/conf/server.xml"
COPY conf/tomcat/Catalina/localhost/rewrite.config "${CATALINA_HOME}/conf/Catalina/localhost/rewrite.config"

RUN apt-get update
RUN apt-get install -y git python zip
RUN /usr/local/jenkins/bin/plugin_install.sh "${JENKINS_STAGING}/plugins"

# Override the default property for DNS lookup caching
RUN echo 'networkaddress.cache.ttl=60' >> ${JAVA_HOME}/jre/lib/security/java.security

CMD /usr/local/jenkins/bin/bootstrap.py && catalina.sh run

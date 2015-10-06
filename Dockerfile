FROM tomcat:8.0.27-jre8

# tomcat:8.0.27-jre8 is based on java:8-jre, which is based on Debian Jessie.
# Let's install a few prerequisite packages that we might find helpful.
RUN apt-get update
RUN apt-get install -y zip

# $CATALINA_HOME is derived from the official Tomcat Dockerfile:
# https://github.com/docker-library/tomcat/blob/df283818c1/8-jre8/Dockerfile
ENV CATALINA_HOME /usr/local/tomcat
ENV PATH $CATALINA_HOME/bin:$PATH
ENV SERVICE_NAME jenkins
WORKDIR $CATALINA_HOME

# Remove the built-in Tomcat apps
RUN rm -rf webapps/*

# Jenkins version and mirror URL
ENV JENKINS_VERSION 1.609.3
ENV JENKINS_MIRROR_BASEURL https://updates.jenkins-ci.org/download/war
ENV JENKINS_WAR_URL $JENKINS_MIRROR_BASEURL/$JENKINS_VERSION/jenkins.war

# Create $JENKINS_HOME as a volume. Since this is the only instance of Jenkins
# that will run in this container, it doesn't seem to be necessary to name
# $JENKINS_HOME after $SERVICE_NAME.
ENV JENKINS_HOME /var/jenkins_home
#VOLUME $JENKINS_HOME

# Download Jenkins and Jenkins plugins
RUN mkdir -p /usr/local/bin
COPY plugin_install.sh /usr/local/bin/plugin_install.sh
RUN set -x && curl -fSL $JENKINS_WAR_URL -o webapps/jenkins.war
RUN /usr/local/bin/plugin_install.sh "${JENKINS_HOME}/plugins"

# Configure Jenkins
COPY config.xml "${JENKINS_HOME}/config.xml"
COPY nodeMonitors.xml "${JENKINS_HOME}/nodeMonitors.xml"

# Configure and run Tomcat
RUN mkdir -p conf/Catalina/localhost
COPY conf/server.xml conf/server.xml
COPY conf/Catalina/localhost/rewrite.config conf/Catalina/localhost/rewrite.config

EXPOSE 8080
CMD ["catalina.sh", "run"]

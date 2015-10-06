FROM tomcat:8.0.27-jre8
WORKDIR /tmp

# tomcat:8.0.27-jre8 is based on java:8-jre, which is based on Debian Jessie.
# Let's install a few prerequisite packages that we might find helpful.
RUN apt-get update
RUN apt-get install -y python zip

# $CATALINA_HOME is derived from the official Tomcat Dockerfile:
# https://github.com/docker-library/tomcat/blob/df283818c1/8-jre8/Dockerfile
ENV CATALINA_HOME /usr/local/tomcat
ENV PATH "${CATALINA_HOME}/bin:${PATH}"

# Remove the built-in Tomcat apps
RUN rm -rf "${CATALINA_HOME}/webapps/*"

# Jenkins version and mirror URL
ENV JENKINS_VERSION 1.609.3
ENV JENKINS_MIRROR_BASEURL https://updates.jenkins-ci.org/download/war
ENV JENKINS_WAR_URL "${JENKINS_MIRROR_BASEURL}/${JENKINS_VERSION}/jenkins.war"

# $JENKINS_STAGING will be used to download plugins and copy config files
#                  during the Docker build process.
#
# $JENKINS_HOME    will be the final destination that Jenkins will use as its
#                  data directory. This cannot be populated before Marathon
#                  has a chance to create the host-container volume mapping.
#
ENV JENKINS_STAGING /var/jenkins_staging
ENV JENKINS_HOME /var/jenkins_home
RUN mkdir -p $JENKINS_HOME

# Download Jenkins and Jenkins plugins
RUN mkdir -p /usr/local/jenkins/bin
COPY plugin_install.sh /usr/local/jenkins/bin/plugin_install.sh
RUN set -x && curl -fSL "$JENKINS_WAR_URL" -o "${CATALINA_HOME}/webapps/jenkins.war"
RUN /usr/local/jenkins/bin/plugin_install.sh "${JENKINS_STAGING}/plugins"

# Configure Jenkins
COPY config.xml "${JENKINS_STAGING}/config.xml"
COPY jenkins.model.JenkinsLocationConfiguration.xml "${JENKINS_STAGING}/jenkins.model.JenkinsLocationConfiguration.xml"
COPY nodeMonitors.xml "${JENKINS_STAGING}/nodeMonitors.xml"
COPY bootstrap.py /usr/local/jenkins/bin/bootstrap.py

# Configure and run Tomcat
RUN mkdir -p "${CATALINA_HOME}/conf/Catalina/localhost"
COPY conf/server.xml "${CATALINA_HOME}/conf/server.xml"
COPY conf/Catalina/localhost/rewrite.config "${CATALINA_HOME}/conf/Catalina/localhost/rewrite.config"

EXPOSE 8080
CMD /usr/local/jenkins/bin/bootstrap.py && catalina.sh run

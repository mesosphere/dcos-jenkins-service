FROM jenkins/jenkins:2.204.6
WORKDIR /tmp

# Environment variables used throughout this Dockerfile
#
# $JENKINS_HOME     will be the final destination that Jenkins will use as its
#                   data directory. This cannot be populated before Marathon
#                   has a chance to create the host-container volume mapping.
#
ENV JENKINS_FOLDER /usr/share/jenkins

# Build Args
ARG BLUEOCEAN_VERSION=1.22.0
ARG JENKINS_STAGING=/usr/share/jenkins/ref/
ARG PROMETHEUS_PLUG_HASH=61ea0cd0bb26d937c8f4df00c7e226c0b51c7b50
ARG STATSD_PLUG_HASH=929d4a6cb3d3ce5f1e03af73075b13687d4879c8
ARG JENKINS_DCOS_HOME=/var/jenkinsdcos_home
ARG user=nobody
ARG uid=99
ARG gid=99

ENV JENKINS_HOME $JENKINS_DCOS_HOME
# Default policy according to https://wiki.jenkins.io/display/JENKINS/Configuring+Content+Security+Policy
ENV JENKINS_CSP_OPTS="sandbox; default-src 'none'; img-src 'self'; style-src 'self';"

USER root

# install dependencies
RUN apt-get update && apt-get install -y nginx python zip jq gettext-base
# update to newer git version
RUN echo "deb http://ftp.debian.org/debian testing main" >> /etc/apt/sources.list \
  && apt-get update && apt-get -t testing install -y git

RUN mkdir -p "${JENKINS_HOME}" "${JENKINS_FOLDER}/war"

# Override the default property for DNS lookup caching
RUN echo 'networkaddress.cache.ttl=60' >> ${JAVA_HOME}/jre/lib/security/java.security

# bootstrap scripts and needed dir setup
COPY scripts/export-libssl.sh /usr/local/jenkins/bin/export-libssl.sh
COPY scripts/dcos-quota.sh /usr/local/jenkins/bin/dcos-quota.sh
COPY scripts/dcos-framework-dns-name.sh /usr/local/jenkins/bin/dcos-framework-dns-name.sh
COPY scripts/dcos-write-known-hosts-file.sh /usr/local/jenkins/bin/dcos-write-known-hosts-file.sh
COPY scripts/run.sh /usr/local/jenkins/bin/run.sh

# nginx setup
RUN mkdir -p /var/log/nginx/jenkins /var/nginx/
COPY conf/nginx/nginx.conf.template /var/nginx/nginx.conf.template

# jenkins setup
ENV CASC_JENKINS_CONFIG /usr/local/jenkins/jenkins.yaml
COPY conf/jenkins/configuration.yaml "${CASC_JENKINS_CONFIG}"
COPY conf/jenkins/jenkins.model.JenkinsLocationConfiguration.xml "${JENKINS_STAGING}/jenkins.model.JenkinsLocationConfiguration.xml"
COPY conf/jenkins/nodeMonitors.xml "${JENKINS_STAGING}/nodeMonitors.xml"
COPY scripts/init.groovy.d/mesos-auth.groovy "${JENKINS_STAGING}/init.groovy.d/mesos-auth.groovy"

# add plugins
COPY plugins.conf /tmp/
RUN sed -i "s/\${BLUEOCEAN_VERSION}/${BLUEOCEAN_VERSION}/g" /tmp/plugins.conf
RUN /usr/local/bin/install-plugins.sh < /tmp/plugins.conf

# Note: There is a cleaner way of accomplishing the following which is documented in https://jira.d2iq.com/browse/DCOS_OSS-5906
ADD https://infinity-artifacts.s3.amazonaws.com/prometheus-jenkins/prometheus.hpi-${PROMETHEUS_PLUG_HASH} "${JENKINS_STAGING}/plugins/prometheus.hpi"
ADD https://infinity-artifacts.s3.amazonaws.com/statsd-jenkins/metrics-graphite.hpi-${STATSD_PLUG_HASH} "${JENKINS_STAGING}/plugins/metrics-graphite.hpi"

# Note: For development purposes, the developer can COPY a pre-release mesos.hpi file into JENKINS_STAGING/plugins/mesos.jpi
# The new naming convention is to use *.jpi files instead of *.hpi files.

RUN chmod -R ugo+rw "$JENKINS_HOME" "${JENKINS_FOLDER}" \
    && chmod -R ugo+r "${JENKINS_STAGING}" \
    && chmod -R ugo+rx /usr/local/jenkins/bin/ \
    && chmod -R ugo+rw /var/jenkins_home/ \
    && chmod -R ugo+rw /var/lib/nginx/ /var/nginx/ /var/log/nginx \
    && chmod ugo+rx /usr/local/jenkins/bin/*

USER ${user}

# disable first-run wizard
RUN echo 2.0 > /usr/share/jenkins/ref/jenkins.install.UpgradeWizard.state

CMD /usr/local/jenkins/bin/run.sh

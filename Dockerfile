FROM jenkins/jenkins:2.150.1
WORKDIR /tmp

# Environment variables used throughout this Dockerfile
#
# $JENKINS_HOME     will be the final destination that Jenkins will use as its
#                   data directory. This cannot be populated before Marathon
#                   has a chance to create the host-container volume mapping.
#
ENV JENKINS_FOLDER /usr/share/jenkins

# Build Args
ARG LIBMESOS_DOWNLOAD_URL=https://downloads.mesosphere.io/libmesos-bundle/libmesos-bundle-1.12.0.tar.gz
ARG BLUEOCEAN_VERSION=1.9.0
ARG JENKINS_STAGING=/usr/share/jenkins/ref/
ARG MESOS_PLUG_HASH=347c1ac133dc0cb6282a0dde820acd5b4eb21133
ARG PROMETHEUS_PLUG_HASH=a347bf2c63efe59134c15b8ef83a4a1f627e3b5d
ARG STATSD_PLUG_HASH=929d4a6cb3d3ce5f1e03af73075b13687d4879c8
ARG JENKINS_DCOS_HOME=/var/jenkinsdcos_home
ARG user=nobody
ARG uid=99
ARG gid=99

ENV JENKINS_HOME $JENKINS_DCOS_HOME
ENV COPY_REFERENCE_FILE_LOG $JENKINS_HOME/copy_reference_file.log
# Default policy according to https://wiki.jenkins.io/display/JENKINS/Configuring+Content+Security+Policy
ENV JENKINS_CSP_OPTS="sandbox; default-src 'none'; img-src 'self'; style-src 'self';"

USER root

# install dependencies
RUN apt-get update && apt-get install -y nginx python zip jq
# libmesos bundle
RUN curl -fsSL "$LIBMESOS_DOWNLOAD_URL" -o libmesos-bundle.tar.gz  \
  && tar -C / -xzf libmesos-bundle.tar.gz  \
  && rm libmesos-bundle.tar.gz
# update to newer git version
RUN echo "deb http://ftp.debian.org/debian testing main" >> /etc/apt/sources.list \
  && apt-get update && apt-get -t testing install -y git

RUN mkdir -p "${JENKINS_HOME}" "${JENKINS_FOLDER}/war"

# Override the default property for DNS lookup caching
RUN echo 'networkaddress.cache.ttl=60' >> ${JAVA_HOME}/jre/lib/security/java.security

# bootstrap scripts and needed dir setup
COPY scripts/bootstrap.py /usr/local/jenkins/bin/bootstrap.py
COPY scripts/export-libssl.sh /usr/local/jenkins/bin/export-libssl.sh
COPY scripts/dcos-account.sh /usr/local/jenkins/bin/dcos-account.sh
COPY scripts/run.sh /usr/local/jenkins/bin/run.sh

# nginx setup
RUN mkdir -p /var/log/nginx/jenkins /var/nginx/
COPY conf/nginx/nginx.conf /var/nginx/nginx.conf

# jenkins setup
COPY conf/jenkins/config.xml "${JENKINS_STAGING}/config.xml"
COPY conf/jenkins/jenkins.model.JenkinsLocationConfiguration.xml "${JENKINS_STAGING}/jenkins.model.JenkinsLocationConfiguration.xml"
COPY conf/jenkins/nodeMonitors.xml "${JENKINS_STAGING}/nodeMonitors.xml"
COPY scripts/init.groovy.d/mesos-auth.groovy "${JENKINS_STAGING}/init.groovy.d/mesos-auth.groovy"

# add plugins
COPY plugins.conf /tmp/
RUN sed -i "s/\${BLUEOCEAN_VERSION}/${BLUEOCEAN_VERSION}/g" /tmp/plugins.conf
RUN /usr/local/bin/install-plugins.sh < /tmp/plugins.conf

# add mesos plugin
ADD https://infinity-artifacts.s3.amazonaws.com/mesos-jenkins/mesos.hpi-${MESOS_PLUG_HASH} "${JENKINS_STAGING}/plugins/mesos.hpi"
ADD https://infinity-artifacts.s3.amazonaws.com/prometheus-jenkins/prometheus.hpi-${PROMETHEUS_PLUG_HASH} "${JENKINS_STAGING}/plugins/prometheus.hpi"
ADD https://infinity-artifacts.s3.amazonaws.com/statsd-jenkins/metrics-graphite.hpi-${STATSD_PLUG_HASH} "${JENKINS_STAGING}/plugins/metrics-graphite.hpi"

# change the config for $user
# alias uid to $uid - should match nobody for host
# set home directory to JENKINS_HOME
# change gid to $gid
RUN groupadd -g ${gid} nobody \
    && usermod -u ${uid} -g ${gid} ${user} \
    && usermod -a -G users nobody \
    && echo "nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin" >> /etc/passwd

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

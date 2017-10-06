FROM jenkins/jenkins:2.73.1
WORKDIR /tmp

# Environment variables used throughout this Dockerfile
#
# $JENKINS_HOME     will be the final destination that Jenkins will use as its
#                   data directory. This cannot be populated before Marathon
#                   has a chance to create the host-container volume mapping.
#
ENV JENKINS_FOLDER /usr/share/jenkins

# Build Args
ARG LIBMESOS_DOWNLOAD_URL=https://downloads.mesosphere.com/libmesos-bundle/libmesos-bundle-1.8.7-1.0.2-2.tar.gz
ARG LIBMESOS_DOWNLOAD_SHA256=9757b2e86c975488f68ce325fdf08578669e3c0f1fcccf24545d3bd1bd423a25
ARG BLUEOCEAN_VERSION=1.2.4
ARG JENKINS_STAGING=/usr/share/jenkins/ref/

USER root

# install dependencies
RUN apt-get update && apt-get install -y nginx python zip jq
# libmesos bundle
RUN curl -fsSL "$LIBMESOS_DOWNLOAD_URL" -o libmesos-bundle.tar.gz  \
  && echo "$LIBMESOS_DOWNLOAD_SHA256 libmesos-bundle.tar.gz" | sha256sum -c - \
  && tar -C / -xzf libmesos-bundle.tar.gz  \
  && rm libmesos-bundle.tar.gz
# update to newer git version
RUN echo "deb http://ftp.debian.org/debian testing main" >> /etc/apt/sources.list \
  && apt-get update && apt-get -t testing install -y git

# Override the default property for DNS lookup caching
RUN echo 'networkaddress.cache.ttl=60' >> ${JAVA_HOME}/jre/lib/security/java.security

# bootstrap scripts and needed dir setup
COPY scripts/bootstrap.py /usr/local/jenkins/bin/bootstrap.py
COPY scripts/export-libssl.sh /usr/local/jenkins/bin/export-libssl.sh
COPY scripts/dcos-account.sh /usr/local/jenkins/bin/dcos-account.sh
RUN mkdir -p "$JENKINS_HOME" "${JENKINS_FOLDER}/war"

# nginx setup
RUN mkdir -p /var/log/nginx/jenkins
COPY conf/nginx/nginx.conf /etc/nginx/nginx.conf

# jenkins setup
COPY conf/jenkins/config.xml "${JENKINS_STAGING}/config.xml"
COPY conf/jenkins/jenkins.model.JenkinsLocationConfiguration.xml "${JENKINS_STAGING}/jenkins.model.JenkinsLocationConfiguration.xml"
COPY conf/jenkins/nodeMonitors.xml "${JENKINS_STAGING}/nodeMonitors.xml"

# add plugins
RUN /usr/local/bin/install-plugins.sh       \
  blueocean-commons:${BLUEOCEAN_VERSION}    \
  blueocean-config:${BLUEOCEAN_VERSION}     \
  blueocean-dashboard:${BLUEOCEAN_VERSION}  \
  blueocean-events:${BLUEOCEAN_VERSION}     \
  blueocean-git-pipeline:${BLUEOCEAN_VERSION}          \
  blueocean-github-pipeline:${BLUEOCEAN_VERSION}       \
  blueocean-i18n:${BLUEOCEAN_VERSION}       \
  blueocean-jwt:${BLUEOCEAN_VERSION}        \
  blueocean-personalization:${BLUEOCEAN_VERSION}    \
  blueocean-pipeline-api-impl:${BLUEOCEAN_VERSION}  \
  blueocean-pipeline-editor:${BLUEOCEAN_VERSION}           \
  blueocean-pipeline-scm-api:${BLUEOCEAN_VERSION}   \
  blueocean-rest-impl:${BLUEOCEAN_VERSION}  \
  blueocean-rest:${BLUEOCEAN_VERSION}       \
  blueocean-web:${BLUEOCEAN_VERSION}        \
  blueocean:${BLUEOCEAN_VERSION}            \
  ant:1.7                        \
  ace-editor:1.1                 \
  ansicolor:0.5.2                \
  antisamy-markup-formatter:1.5  \
  artifactory:2.12.2             \
  authentication-tokens:1.3      \
  azure-credentials:1.2          \
  azure-vm-agents:0.4.7.1        \
  branch-api:2.0.11              \
  build-name-setter:1.6.7        \
  build-timeout:1.18             \
  cloudbees-folder:6.1.2         \
  conditional-buildstep:1.3.6    \
  config-file-provider:2.16.3    \
  copyartifact:1.38.1            \
  cvs:2.13                       \
  docker-build-publish:1.3.2     \
  docker-workflow:1.13           \
  durable-task:1.14              \
  ec2:1.36                       \
  embeddable-build-status:1.9    \
  external-monitor-job:1.7       \
  ghprb:1.39.0                   \
  git:3.5.1                      \
  git-client:2.5.0               \
  git-server:1.7                 \
  github:1.28.0                  \
  github-api:1.86                \
  github-branch-source:2.2.3     \
  github-organization-folder:1.6 \
  gitlab:1.4.8                   \
  gradle:1.27.1                  \
  greenballs:1.15                \
  handlebars:1.1.1               \
  ivy:1.27.1                     \
  jackson2-api:2.7.3             \
  job-dsl:1.65                   \
  jobConfigHistory:2.17          \
  jquery:1.11.2-1                \
  ldap:1.17                      \
  mapdb-api:1.0.9.0              \
  marathon:1.6.0                 \
  matrix-auth:1.7                \
  matrix-project:1.11            \
  maven-plugin:2.17              \
  mesos:0.15.0                   \
  metrics:3.1.2.10               \
  momentjs:1.1.1                 \
  monitoring:1.69.0              \
  nant:1.4.3                     \
  node-iterator-api:1.5.0        \
  pam-auth:1.3                   \
  parameterized-trigger:2.35.2   \
  pipeline-build-step:2.5.1      \
  pipeline-github-lib:1.0        \
  pipeline-input-step:2.8        \
  pipeline-milestone-step:1.3.1  \
  pipeline-model-api:1.1.9       \
  pipeline-model-definition:1.1.9 \
  pipeline-model-extensions:1.1.9 \
  pipeline-rest-api:2.9          \
  pipeline-stage-step:2.2        \
  pipeline-stage-view:2.9        \
  plain-credentials:1.4          \
  rebuild:1.25                   \
  role-strategy:2.6.0            \
  run-condition:1.0              \
  s3:0.10.12                     \
  saferestart:0.3                \
  saml:1.0.4                     \
  scm-api:2.2.2                  \
  ssh-agent:1.15                 \
  ssh-slaves:1.21                \
  subversion:2.9                 \
  timestamper:1.8.8              \
  translation:1.15               \
  variant:1.1                    \
  windows-slaves:1.3.1           \
  workflow-aggregator:2.5        \
  workflow-api:2.20              \
  workflow-basic-steps:2.6       \
  workflow-cps:2.40              \
  workflow-cps-global-lib:2.9    \
  workflow-durable-task-step:2.15 \
  workflow-job:2.14.1            \
  workflow-multibranch:2.16      \
  workflow-scm-step:2.6          \
  workflow-step-api:2.12         \
  workflow-support:2.14

# disable first-run wizard
RUN echo 2.0 > /usr/share/jenkins/ref/jenkins.install.UpgradeWizard.state

CMD export LD_LIBRARY_PATH=/libmesos-bundle/lib:/libmesos-bundle/lib/mesos:$LD_LIBRARY_PATH \
  && export MESOS_NATIVE_JAVA_LIBRARY=$(ls /libmesos-bundle/lib/libmesos-*.so)   \
  && . /usr/local/jenkins/bin/export-libssl.sh       \
  && /usr/local/jenkins/bin/bootstrap.py && nginx    \
  && . /usr/local/jenkins/bin/dcos-account.sh        \
  && java ${JVM_OPTS}                                \
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

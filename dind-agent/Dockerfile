FROM docker:1.10-dind

# Please keep each package list in alphabetical order
# Required dependencies for the jenkins agent
RUN apk --update add \
bash \
openjdk8-jre \
openssh-client
# Optional convenience functions used by most builds
RUN apk --update add \
git \
jq \
python \
python3 \
unzip

COPY wrapper.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wrapper.sh

# Add any SSH known hosts to the environment variable $SSH_KNOWN_HOSTS
ENV SSH_KNOWN_HOSTS github.com
RUN ssh-keyscan $SSH_KNOWN_HOSTS | tee /etc/ssh/ssh_known_hosts

ENTRYPOINT []
CMD []

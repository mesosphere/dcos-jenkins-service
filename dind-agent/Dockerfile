FROM docker:1.10-dind
# include dependencies needed by the jenkins agent itself
RUN apk --update add openjdk8-jre unzip git python python3 bash jq openssh-client

COPY wrapper.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wrapper.sh

# Add any SSH known hosts to the environment variable $SSH_KNOWN_HOSTS
ENV SSH_KNOWN_HOSTS github.com
RUN ssh-keyscan $SSH_KNOWN_HOSTS | tee /etc/ssh/ssh_known_hosts

ENTRYPOINT []
CMD []

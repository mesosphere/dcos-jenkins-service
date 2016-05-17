#!/bin/bash
set -o errexit -o nounset -o pipefail

# vars
readonly DOCKER_IMAGE="mesosphere/jenkins"
readonly TAG=${GIT_BRANCH##*/}
readonly TAR_FILE="velocity-${TAG}.tar"

# docker pieces
docker login --email="$DOCKER_HUB_EMAIL" --username="$DOCKER_HUB_USERNAME" --password="$DOCKER_HUB_PASSWORD"
docker build -t $DOCKER_IMAGE:$TAG .
docker push $DOCKER_IMAGE:$TAG
docker save --output="${TAR_FILE}" $DOCKER_IMAGE:$TAG

# check integrity
tar tf $TAR_FILE > /dev/null
# gzip with best compression
gzip -9 $TAR_FILE

# generate sigs
openssl md5 $TAR_FILE.gz >> jenkins-$TAG.checksums
openssl sha1 $TAR_FILE.gz >> jenkins-$TAG.checksums

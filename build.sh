#!/bin/bash

set -e

# If DOCKER_IMAGE envvar set then use that
# Else build DOCKER_IMAGE

if [ -n "${DOCKER_IMAGE}" ]; then
	# DOCKER_IMAGE envvar is user supplied
    echo "Using DOCKER_IMAGE : $DOCKER_IMAGE"
else
	echo "Building docker image..."
	# docker publish to user docker repo (e.g. DOCKER_REPO envvar)
	: ${DOCKER_REPO?"Need to set DOCKER_REPO env var as DOCKER_IMAGE is not specified"}

	if [ -n "${DOCKER_TAG}" ]; then
		echo "Using DOCKER_TAG : $DOCKER_TAG"
		DOCKER_IMAGE="${DOCKER_REPO}/jenkins-dev:${DOCKER_TAG}"
	else
		TAG=`git rev-parse HEAD`
		DOCKER_IMAGE="${DOCKER_REPO}/jenkins-dev:${TAG}"
	fi

	# docker build and publish
    echo Building $DOCKER_IMAGE
	docker build -t "${DOCKER_IMAGE}" .
    echo Pushing $DOCKER_IMAGE
	docker push "${DOCKER_IMAGE}"
fi

# Use tooling to reference the correct image (via templating) and publish stub
env TEMPLATE_DOCKER-IMAGE="${DOCKER_IMAGE}" tools/publish_aws.py jenkins stub-universe-all-ucr universe/

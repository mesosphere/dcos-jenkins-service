#!/bin/bash

# If DOCKER_IMAGE envvar set then use that
# Else build DOCKER_IMAGE

# docker build
docker build .

# docker publish to user docker repo (e.g. DOCKER_REPO envvar)
# TODO Colin or Tarun

# Set DOCKER_IMAGE envvar to value user supplied
# TODO Colin or Tarun

# Update universe/ or using tooling to reference the correct image (via templating)
# TODO Tarun

# Publish stub
tools/publish_aws.py jenkins universe/

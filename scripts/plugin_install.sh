#!/bin/bash
# Download a number of Jenkins plugins to a particular directory, specified as
# an argument to this script. If no path is provided, default to the current
# working directory.
#
#   Example usage: ./plugin_install.sh [/path/to/plugins_dir]
#
set -e
set -x

JENKINS_PLUGINS_DIR="${1-$PWD}"
JENKINS_PLUGINS_MIRROR="https://updates.jenkins-ci.org/download/plugins"

# Jenkins plugins are specified here, following the format "pluginname/version"
JENKINS_PLUGINS=(
    "ansicolor/0.4.2"
    "credentials/1.23"
    "git/2.4.0"
    "git-client/1.19.0"
    "greenballs/1.14"
    "job-dsl/1.38"
    "mesos/0.9.0"
    "monitoring/1.57.0"
    "parameterized-trigger/2.29"
    "rebuild/1.25"
    "saferestart/0.3"
    "scm-api/0.2"
    "script-security/1.15"
    "ssh-credentials/1.11"
    "token-macro/1.10"
)

# Create $JENKINS_PLUGINS_DIR if it doesn't exist
if [[ ! -d "$JENKINS_PLUGINS_DIR" ]]; then
    mkdir -p "$JENKINS_PLUGINS_DIR"
fi

# Download each of the plugins specified in $JENKINS_PLUGINS
for plugin in ${JENKINS_PLUGINS[@]}; do
    IFS='/' read -a plugin_info <<< "${plugin}"
    plugin_remote_path="${plugin_info[0]}/${plugin_info[1]}/${plugin_info[0]}.hpi"
    plugin_local_path="${JENKINS_PLUGINS_DIR}/${plugin_info[0]}.hpi"
    curl -fSL "${JENKINS_PLUGINS_MIRROR}/${plugin_remote_path}" -o $plugin_local_path

    # All Jenkins .hpi/.jpi files are actually Zip files. Let's check their
    # integrity during the build process so we dont have any surprises at
    # container run time.
    zip --test $plugin_local_path
done

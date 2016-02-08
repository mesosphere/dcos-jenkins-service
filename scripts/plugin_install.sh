#!/bin/bash
# Download a number of Jenkins plugins to a particular directory, specified as
# an argument to this script. If no path is provided, default to the current
# working directory.
#
#   Example usage: ./plugin_install.sh [/path/to/plugins_dir]
#
set -e
#set -x

JENKINS_PLUGINS_DIR="${1-$PWD}"
JENKINS_PLUGINS_MIRROR="https://updates.jenkins-ci.org/download/plugins"
JENKINS_UPDATE_CENTER_JSON=$(curl -sL https://updates.jenkins-ci.org/update-center.json | sed '1d;$d')

# Jenkins plugins are specified here, following the format "pluginname/version"
JENKINS_PLUGINS=(
    "ansicolor/0.4.2"
    "credentials/1.24"
    "git/2.4.1"
    "git-client/1.19.2"
    "greenballs/1.15"
    "job-dsl/1.42"
    "jobConfigHistory/2.12"
    "mesos/0.10.0"
    "monitoring/1.58.0"
    "parameterized-trigger/2.30"
    "rebuild/1.25"
    "saferestart/0.3"
    "scm-api/0.2"
    "script-security/1.17"
    "ssh-credentials/1.11"
    "token-macro/1.12.1"
)

# Create $JENKINS_PLUGINS_DIR if it doesn't exist
if [[ ! -d "$JENKINS_PLUGINS_DIR" ]]; then
    mkdir -p "$JENKINS_PLUGINS_DIR"
fi

function check_for_update {
    plugin_name=$1
    plugin_ver=$2

    latest_plugin_ver=$(echo $JENKINS_UPDATE_CENTER_JSON | jq -r ".plugins | .[\"${plugin_name}\"] | .version")
    if [[ $plugin_ver == $latest_plugin_ver ]]; then
        echo "${plugin_name} is up to date."
    else
        echo "WARNING: ${plugin_name} is not up to date. Pinned version: ${plugin_ver}. Latest version: ${latest_plugin_ver}"
    fi
}

# Download each of the plugins specified in $JENKINS_PLUGINS
for plugin in ${JENKINS_PLUGINS[@]}; do
    IFS='/' read -a plugin_info <<< "${plugin}"
    plugin_name=${plugin_info[0]}
    plugin_ver=${plugin_info[1]}

    plugin_remote_path="${plugin_name}/${plugin_ver}/${plugin_name}.hpi"
    plugin_local_path="${JENKINS_PLUGINS_DIR}/${plugin_name}.hpi"

    echo "Downloading ${plugin_name} ${plugin_ver} ..."
    check_for_update $plugin_name $plugin_ver
    curl -fSL "${JENKINS_PLUGINS_MIRROR}/${plugin_remote_path}" -o $plugin_local_path 2> /dev/null

    # All Jenkins .hpi/.jpi files are actually Zip files. Let's check their
    # integrity during the build process so we dont have any surprises at
    # container run time.
    zip --test $plugin_local_path

    echo
done

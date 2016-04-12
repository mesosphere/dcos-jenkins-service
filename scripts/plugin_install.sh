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
    "ansicolor~0.4.2"
    "artifactory~2.4.7"
    "build-pipeline-plugin~1.5.2"
    "credentials~1.26"
    "credentials-binding~1.7"
    "embeddable-build-status~1.9"
    "ghprb~1.31.3"
    "git~2.4.4"
    "git-client~1.19.6"
    "github~1.18.1"
    "github-api~1.72.1"
    "greenballs~1.15"
    "jquery~1.11.2-0"
    "job-dsl~1.44"
    "jobConfigHistory~2.13"
    "mesos~0.12.0"
    "monitoring~1.59.0"
    "parameterized-trigger~2.30"
    "plain-credentials~1.1"
    "rebuild~1.25"
    "role-strategy~2.2.0"
    "saferestart~0.3"
    "saml~0.5"
    "scm-api~0.2"
    "script-security~1.17"
    "ssh-credentials~1.11"
    "token-macro~1.12.1"
    "workflow-step-api~1.15"
    "marathon~1.1~https://s3.amazonaws.com/downloads.mesosphere.io/velocity/jenkins/plugins/marathon-1.1.hpi"
)

# Create $JENKINS_PLUGINS_DIR if it doesn't exist
if [[ ! -d "$JENKINS_PLUGINS_DIR" ]]; then
    mkdir -p "$JENKINS_PLUGINS_DIR"
fi

# Check the Update Center JSON for latest version of plugin
# and compare against the configured version in JENKINS_PLUGINS
function check_for_update {
    plugin_name=$1
    plugin_ver=$2

    local latest_plugin_ver=$(echo $JENKINS_UPDATE_CENTER_JSON | jq -r ".plugins | .[\"${plugin_name}\"] | .version")
    if [[ $plugin_ver == $latest_plugin_ver ]]; then
        echo "${plugin_name} is up to date."
    else
        echo "WARNING: ${plugin_name} is not up to date. Pinned version: ${plugin_ver}. Latest version: ${latest_plugin_ver}"
    fi
}

# Set variables for the passed-in plugin, which is
# an element from the JENKINS_PLUGINS array.
function set_plugin_vars {
    local plugin=$1
    IFS='~' read -a plugin_info <<< "${plugin}"
    plugin_name=${plugin_info[0]}
    plugin_ver=${plugin_info[1]}
    plugin_url=${plugin_info[2]}
    plugin_local_path="${JENKINS_PLUGINS_DIR}/${plugin_name}.hpi"
    plugin_remote_path="${plugin_name}/${plugin_ver}/${plugin_name}.hpi"
}

# Download the hpi file from the given url.
function fetch_plugin_hpi {
    curl -fSL "${1}" -o $plugin_local_path 2> /dev/null
}

# Check the integrity of a downloaded zip file.
function test_zip {
    # All Jenkins .hpi/.jpi files are actually Zip files. Let's check their
    # integrity during the build process so we dont have any surprises at
    # container run time.
    zip --test "${1}"
}

# Download each of the plugins specified in $JENKINS_PLUGINS
for plugin in ${JENKINS_PLUGINS[@]}; do
    set_plugin_vars $plugin

    echo "Downloading ${plugin_name} ${plugin_ver} ..."

    # if $plugin_url is null, then grab it from Update Center
    # otherwise, download from the given url
    if [[ -z $plugin_url ]]; then
        check_for_update $plugin_name $plugin_ver
        fetch_plugin_hpi "${JENKINS_PLUGINS_MIRROR}/${plugin_remote_path}"
    else
        fetch_plugin_hpi $plugin_url
    fi
    test_zip $plugin_local_path

    echo
done

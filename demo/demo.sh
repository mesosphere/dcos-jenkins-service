#!/bin/bash
set -e

function usage {
    cat <<END
Usage: $0 <create|cleanup> <http://jenkins.url:port>

This script will create 50 "freestyle" Jenkins jobs. Each of these jobs will
appear as a separate Jenkins build, and will randomly pass or fail. The
duration of each job will be between 120 and 240 seconds.

When combined with Apache Mesos or the Mesosphere DCOS, this script will demo
how the Mesos plugin can automatically create and destroy Jenkins build slaves
as demand increases or decreases.
END
    return 1
}

function verify_jenkins {
    local jenkins_url=$1

    if jenkins_version=`curl -sI $jenkins_url | grep 'X-Jenkins:' | awk -F': ' '{print $2}' | tr -d '\r'`; then
        echo "Info: Jenkins is up and running! Got Jenkins version ${jenkins_version}."
        echo
    else
        echo "Error: didn't find a Jenkins instance running at ${jenkins_url}."
        return 1
    fi
}

function create {
    local jenkins_url=$1
    local job_basename=$2
    local count=$3

    cat << END
This script will create 50 "freestyle" Jenkins jobs. Each of these jobs will
appear as a separate Jenkins build, and will randomly pass or fail. The
duration of each job will be between 120 and 240 seconds.

About to create ${count} jobs that start with ${job_basename} on the Jenkins
instance located at:

  ${jenkins_url}

END

    read -p "Press [Enter] to continue, or ^C to cancel..."

    for i in `seq -f "%02g" 1 $count`; do
        duration=$(((RANDOM % 120) + 120))
        result=$((RANDOM % 2))
        demo_job_name="${job_basename}-${i}"

        curl -fH 'Content-Type: application/xml' --data-binary @demo-job.xml \
            "${jenkins_url}/createItem?name=${demo_job_name}"

        if [[ $? == 0 ]]; then
            echo "Job '${demo_job_name}' created successfully. Duration: ${duration}. Result: ${result}. Triggering build."
            curl -fX POST "${jenkins_url}/job/${demo_job_name}/buildWithParameters?DURATION=${duration}&RESULT=${result}"
        else
            echo "There was a problem creating the Jenkins job '${demo_job_name}'."
            return 1
        fi
    done
}

function cleanup {
    local jenkins_url=$1
    local job_basename=$2
    local count=$3

    for i in `seq -f "%02g" 1 $count`; do
        demo_job_name="${job_basename}-${i}"
        echo "Deleting job '${demo_job_name}'"
        curl -fX POST "${jenkins_url}/job/${demo_job_name}/doDelete"
    done
}

function main {
    local demo_job_name="demo-job"
    local demo_job_count=50

    if ! command -v curl > /dev/null; then
        echo "Error: cURL not found in $PATH"
        return 1
    fi

    if [[ ! $# != 4 ]]; then
        usage
    else
        local operation="$1"
        local jenkins_url="$2"
    fi

    case $operation in
        create)
            verify_jenkins $jenkins_url
            create $jenkins_url $demo_job_name $demo_job_count
            ;;
        cleanup)
            verify_jenkins $jenkins_url
            cleanup $jenkins_url $demo_job_name $demo_job_count
            ;;
        *)
            echo -e "Unknown operation: ${operation}\n"
            usage
            ;;
    esac


}

main $@

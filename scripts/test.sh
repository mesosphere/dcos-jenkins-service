#!/bin/bash
set +x -e -o pipefail
declare -i poll_period=10
declare -i seconds_until_timeout=$((60 * 30))

CLUSTER_ID=$(http \
    --ignore-stdin                                 \
    "https://ccm.mesosphere.com/api/cluster/"      \
    "Authorization:Token ${CCM_AUTH_TOKEN}"        \
    "name=${JOB_NAME##*/}-${BUILD_NUMBER}"         \
    "cluster_desc=${JOB_NAME##*/} ${BUILD_NUMBER}" \
    time=60                                        \
    cloud_provider=0                               \
    region=us-west-2                               \
    channel=testing/master                         \
    template=ee.single-master.cloudformation.json  \
    adminlocation=0.0.0.0/0                        \
    public_agents=0                                \
    private_agents=1                               \
    | jq ".id"
)

echo "Waiting for DC/OS cluster to form... (ID: ${CLUSTER_ID})"

while (("$seconds_until_timeout" >= "0")); do
    STATUS=$(http \
        --ignore-stdin \
        "https://ccm.mesosphere.com/api/cluster/${CLUSTER_ID}/" \
        "Authorization:Token ${CCM_AUTH_TOKEN}" \
        | jq ".status"
    )

    if [[ ${STATUS} -eq 0 ]]; then
        break
    elif [[ ${STATUS} -eq 7 ]]; then
        echo "ERROR: cluster creation failed."
        exit 7
    fi

    sleep $poll_period
    let "seconds_until_timeout -= $poll_period"
done

if (("$seconds_until_timeout" <= "0")); then
    echo "ERROR: timed out waiting for cluster."
    exit 2
fi

CLUSTER_INFO=$(http                                         \
    --ignore-stdin                                          \
    "https://ccm.mesosphere.com/api/cluster/${CLUSTER_ID}/" \
    "Authorization:Token ${CCM_AUTH_TOKEN}"                 \
    | jq -r ".cluster_info"
)

DCOS_URL="http://$(echo "${CLUSTER_INFO}" | jq -r ".DnsAddress")"

ln -s $DOT_SHAKEDOWN ~/.shakedown
TERM=velocity shakedown --stdout all --ssh-key-file $CLI_TEST_SSH_KEY --dcos-url $DCOS_URL

http                                                        \
    --ignore-stdin                                          \
    DELETE                                                  \
    "https://ccm.mesosphere.com/api/cluster/${CLUSTER_ID}/" \
    "Authorization:Token ${CCM_AUTH_TOKEN}"

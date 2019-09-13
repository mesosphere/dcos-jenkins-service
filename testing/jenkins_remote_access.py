#!/usr/bin/env python3

import logging
from string import Template

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(message)s")


IMPORTS = """
import org.jenkinsci.plugins.mesos.MesosCloud;
import org.jenkinsci.plugins.mesos.MesosSlaveInfo;
import org.apache.mesos.Protos;
import hudson.slaves.NodeProperty;
import jenkins.model.*
import org.jenkinsci.plugins.mesos.MesosSlaveInfo.URI;
import hudson.tasks.*;
import com.cloudbees.hudson.plugins.folder.Folder;
"""

DOCKER_CONTAINER = """
def containerInfo = new MesosSlaveInfo.ContainerInfo(
                "MESOS",
                "$dockerImage",
                true,
                false,
                false,
                true,
                "wrapper.sh",
                new LinkedList<MesosSlaveInfo.Volume>(),
                new LinkedList<MesosSlaveInfo.Parameter>(),
                Protos.ContainerInfo.DockerInfo.Network.BRIDGE.name(),
                new LinkedList<MesosSlaveInfo.PortMapping>(),
                new LinkedList<MesosSlaveInfo.NetworkInfo>()
)
"""

MESOS_SLAVE_INFO_OBJECT = """
def additionalURIs = new LinkedList<URI>()
additionalURIs.add(new URI("file:///etc/docker/docker.tar.gz", false, true))

def mesosSlaveInfo = new MesosSlaveInfo(
        "$labelString",
        $mode,
        "$slaveCpus",
        "$slaveMem",
        "$minExecutors",
        "$maxExecutors",
        "$executorCpus",
        "$diskNeeded",
        "$executorMem",
        "$remoteFSRoot",
        "$idleTerminationMinutes",
        "$slaveAttributes",
        "$jvmArgs",
        "$jnlpArgs",
        "$defaultSlave",
        $containerInfo,
        new LinkedList<URI>(),
        new LinkedList<? extends NodeProperty<?>>()
)
"""

MESOS_SLAVE_INFO_ADD = """
MesosCloud cloud = MesosCloud.get();
cloud.getSlaveInfos().add(mesosSlaveInfo)
cloud.getSlaveInfos().each {
        t ->
            println("Label : " + t.getLabelString())
}
"""

MESOS_SLAVE_INFO_REMOVE = """
MesosCloud cloud = MesosCloud.get();
Iterator<MesosSlaveInfo> it = cloud.getSlaveInfos().iterator()
while(it.hasNext()) {
    MesosSlaveInfo msi = it.next();
    if (msi.getLabelString().equals("$labelString")){
        it.remove()
    }
}
cloud.getSlaveInfos().each {
        t ->
            println("Label : " + t.getLabelString())
}
"""

DELETE_ALL_JOBS = """
Jenkins.instance.items.each { job -> job.delete() }
"""

JENKINS_JOB_FAILURES = """
def activeJobs = hudson.model.Hudson.instance.items.findAll{job -> !(job instanceof Folder) && job.isBuildable()}
println("successjobs = " +activeJobs.size())
def failedRuns = activeJobs.findAll{job -> job.lastBuild != null && !(job.lastBuild.isBuilding()) && job.lastBuild.result == hudson.model.Result.FAILURE}
println("failedjobs = " +failedRuns.size())
BUILD_STRING = "Build step 'Execute shell' marked build as failure"

failedRuns.each{ item ->
    println "Failed Job Name: ${item.name}"
    item.lastBuild.getLog().eachLine { line ->
        if (line =~ /$BUILD_STRING/) {
            println "error: $line"
        }
    }
}
"""

CREDENTIAL_CHANGE = """
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl

MesosCloud cloud = MesosCloud.get();

def changePassword = { new_username, new_password ->
    def c = cloud.credentials

    if ( c ) {
        def credentials_store = Jenkins.instance.getExtensionList(
            'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
            )[0].getStore()

        def result = credentials_store.updateCredentials(
            com.cloudbees.plugins.credentials.domains.Domain.global(), 
            c, 
            new UsernamePasswordCredentialsImpl(c.scope, c.id, c.description, new_username, new_password)
            )

        if (result) {
            println "changed jenkins creds" 
        } else {
            println "failed to change jenkins creds"
        }
    } else {
      println "could not find credential for jenkins"
    }
}

changePassword('$userName', 'abcdefg')

cloud.restartMesos()
"""


CREDENTIAL_CHANGE = """
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl

MesosCloud cloud = MesosCloud.get();

def changePassword = { new_username, new_password ->
    def c = cloud.credentials

    if ( c ) {
        def credentials_store = Jenkins.instance.getExtensionList(
            'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
            )[0].getStore()

        def result = credentials_store.updateCredentials(
            com.cloudbees.plugins.credentials.domains.Domain.global(), 
            c, 
            new UsernamePasswordCredentialsImpl(c.scope, c.id, c.description, new_username, new_password)
            )

        if (result) {
            println "changed jenkins creds" 
        } else {
            println "failed to change jenkins creds"
        }
    } else {
      println "could not find credential for jenkins"
    }
}

changePassword('$userName', 'abcdefg')

cloud.restartMesos()
"""


def add_slave_info(
        labelString,
        service_name,
        dockerImage="mesosphere/jenkins-dind:0.7.0-ubuntu",
        slaveCpus="0.1",
        slaveMem="256",
        minExecutors="1",
        maxExecutors="1",
        executorCpus="0.4",
        diskNeeded="0.0",
        executorMem="512",
        mode="Node.Mode.NORMAL",
        remoteFSRoot="jenkins",
        idleTerminationMinutes="5",
        slaveAttributes="",
        jvmArgs="-Xms16m -XX:+UseConcMarkSweepGC -Djava.net.preferIPv4Stack=true",
        jnlpArgs="-noReconnect",
        defaultSlave="false",
        **kwargs
):
    slaveInfo = Template(MESOS_SLAVE_INFO_OBJECT).substitute({
         "labelString": labelString,
         "mode": mode,
         "slaveCpus": slaveCpus,
         "slaveMem": slaveMem,
         "minExecutors": minExecutors,
         "maxExecutors": maxExecutors,
         "executorCpus": executorCpus,
         "diskNeeded": diskNeeded,
         "executorMem": executorMem,
         "remoteFSRoot": remoteFSRoot,
         "idleTerminationMinutes": idleTerminationMinutes,
         "slaveAttributes": slaveAttributes,
         "jvmArgs": jvmArgs,
         "jnlpArgs": jnlpArgs,
         "defaultSlave": defaultSlave,
         "containerInfo": "containerInfo",
    })

    containerInfo = Template(DOCKER_CONTAINER).substitute({
        "dockerImage": dockerImage,
    })

    return make_post(
        containerInfo +
        slaveInfo +
        MESOS_SLAVE_INFO_ADD,
        service_name,
        **kwargs,
    )


def remove_slave_info(labelString, service_name):
    return make_post(
        Template(MESOS_SLAVE_INFO_REMOVE).substitute(
            {
                'labelString': labelString
            }
        ),
        service_name
    )


def delete_all_jobs(**kwargs):
    return make_post(DELETE_ALL_JOBS, **kwargs)


def get_job_failures(service_name):
    return make_post(JENKINS_JOB_FAILURES, service_name)


def change_mesos_creds(mesos_username, service_name):
    return make_post(
        Template(CREDENTIAL_CHANGE).substitute(
            {
                'userName': mesos_username,
            }
        ),
        service_name)


def change_mesos_creds(mesos_username, service_name):
    return make_post(
        Template(CREDENTIAL_CHANGE).substitute(
            {
                'userName': mesos_username,
            }
        ),
        service_name)


def make_post(
        post_body,
        service_name,
        **kwargs
):
    """
    :rtype: requests.Response
    """
    body = IMPORTS + post_body
    log.info('\nMaking request : ========\n{}\n========\n'.format(body))
    '''
    Note: To run locally:
    curl -i -H "Authorization:token=$(dcos config show core.dcos_acs_token)" \
         -k --data-urlencode "script=$(< <path-to-above-script-file>)" \
         https://<dcos-cluster>/service/jenkins/scriptText'
    '''
    import sdk_cmd
    return sdk_cmd.service_request(
        'POST',
        service_name,
        'scriptText',
        log_args=False,
        data={'script': body},
        **kwargs,
    )

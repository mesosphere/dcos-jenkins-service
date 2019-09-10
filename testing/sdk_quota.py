"""Utilities relating to interaction with Mesos quota

************************************************************************
FOR THE TIME BEING WHATEVER MODIFICATIONS ARE APPLIED TO THIS FILE
SHOULD ALSO BE APPLIED TO sdk_plan IN ANY OTHER PARTNER REPOS
************************************************************************
"""
import enum
import logging
import json

import sdk_cmd

from enum import Enum

log = logging.getLogger(__name__)


class QuotaType(Enum):
    GUARANTEE = 1
    LIMIT = 2


def create_quota(role: str, cpus=0.0, mem=0, gpus=0, quota_type=QuotaType.GUARANTEE):
    """ Used to create a Mesos quota for the specificed role.

    :param role: the role to create quota for
    :param cpus: the amount of cpus
    :param mem: the amount of memory
    :param gpus: the amount of GPUs

    Raises an exception on failure
    """
    if cpus == 0.0 and mem == 0.0 and gpus == 0.0:
        log.info(
            "create_quota called with cpus, mem, and gpus all 0.0. Not creating any quota."
        )
    if quota_type is QuotaType.GUARANTEE:
        guarantee = []
        if cpus != 0.0:
            guarantee.append(_create_guarantee("cpus", cpus))
        if mem != 0:
            guarantee.append(_create_guarantee("mem", mem))
        if gpus != 0:
            guarantee.append(_create_guarantee("gpus", gpus))

        log.info(
            "Creating quota guarantee for role %s. cpus: %s mem: %s gpus: %s",
            role,
            cpus,
            mem,
            gpus,
        )
        sdk_cmd.cluster_request(
            "POST", "/mesos/quota", json=_create_quota_request(role, guarantee)
        )

    else:
        # Limits right now queries the mesos/api/v1 endpoint till
        # the mesos/quota enpoint is built out. This code should
        # be restructured to use the /quota endpoint when ready.
        log.info(
            "Creating quota limit for role %s. cpus: %s mem: %s gpus: %s",
            role,
            cpus,
            mem,
            gpus,
        )
        sdk_cmd.cluster_request(
            "POST",
            "/mesos/api/v1",
            json=_create_quota_limit_request(role, cpus, mem, gpus),
        )
    log.info("Quota created for role %s", role)


def remove_quota(role: str):
    """ Removes any quota for the specified role

    :param role: the role to remove quota from
    """
    log.info("Removing quota for role %s", role)
    sdk_cmd.cluster_request("DELETE", "/mesos/quota/{}".format(role))
    log.info("Quota removed for role %s", role)


def list_quotas() -> dict:
    log.info("Listing all quota")
    return json.loads(sdk_cmd.cluster_request("GET", "/mesos/quota").text)


def _create_quota_request(role: str, guarantee: list):
    return {"role": role, "guarantee": guarantee}


def _create_guarantee(type: str, value: float):
    return {"name": type, "type": "SCALAR", "scalar": {"value": value}}


def _create_quota_limit_request(role: str, cpus: float, mem: float, gpus: float):
    limits = {}
    if cpus != 0.0:
        limits["cpus"] = {"value": cpus}
    if mem != 0:
        limits["mem"] = {"value": mem}
    if gpus != 0:
        limits["gpus"] = {"value": gpus}

    return {
        "type": "UPDATE_QUOTA",
        "update_quota": {"quota_configs": [{"role": role, "limits": limits}]},
    }

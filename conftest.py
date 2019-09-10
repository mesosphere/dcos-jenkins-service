import logging
import os
import pytest
import sys

log_level = os.getenv("TEST_LOG_LEVEL", "INFO").upper()
log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "EXCEPTION")
assert log_level in log_levels, "{} is not a valid log level. Use one of: {}".format(
    log_level, ", ".join(log_levels)
)
# write everything to stdout due to the following circumstances:
# - shakedown uses print() aka stdout
# - teamcity splits out stdout vs stderr into separate outputs, we'd want them combined
logging.basicConfig(
    format="[%(asctime)s|%(name)s|%(levelname)s]: %(message)s",
    level=log_level,
    stream=sys.stdout,
)


def pytest_addoption(parser):
    parser.addoption(
        "--masters",
        action="store",
        default=1,
        type=int,
        help="Number of Jenkins masters to launch.",
    )
    parser.addoption(
        "--jobs",
        action="store",
        default=1,
        type=int,
        help="Number of test jobs to launch.",
    )
    parser.addoption(
        "--single-use", action="store_true", help="Use Mesos Single-Use agents"
    )
    parser.addoption(
        "--run-delay",
        action="store",
        default=1,
        type=int,
        help="Run job every X minutes.",
    )
    parser.addoption(
        "--cpu-quota",
        action="store",
        default=0.0,
        type=float,
        help="CPU quota to set. 0.0 to set no" " quota.",
    )
    parser.addoption(
        "--memory-quota",
        action="store",
        default=0.0,
        type=float,
        help="Memory quota to set. 0.0 to set no" " quota.",
    )
    parser.addoption(
        "--work-duration",
        action="store",
        default=600,
        type=int,
        help="Duration, in seconds, for the " "workload to last (sleep).",
    )
    parser.addoption(
        "--mom", action="store", default="", help="Marathon on Marathon instance name."
    )
    parser.addoption(
        "--external-volume", action="store_true", help="Use rexray external volumes."
    )
    parser.addoption(
        "--scenario",
        action="store",
        default="sleep",
        help="Test scenario to run (sleep, buildmarathon) " "(default: sleep).",
    )
    parser.addoption(
        "--min",
        action="store",
        default=-1,
        help="min jenkins index to start from" "(default: -1).",
    )
    parser.addoption(
        "--max",
        action="store",
        default=-1,
        help="max jenkins index to end at" "(default: -1).",
    )
    parser.addoption(
        "--batch-size",
        action="store",
        default=1,
        help="batch size to deploy jenkins masters in" "(default: 1).",
    )
    parser.addoption(
        "--service-ids",
        action="store",
        default="",
        help="list of jenkins masters to delete",
    )

    parser.addoption(
        "--enforce-quota-guarantee",
        action="store",
        default=True,
        type=bool,
        help="Set quota values as guarantee.",
    )

    parser.addoption(
        "--enforce-quota-limit",
        action="store",
        default=True,
        type=bool,
        help="Set quota values as limit.",
    )


@pytest.fixture
def master_count(request) -> int:
    return int(request.config.getoption("--masters"))


@pytest.fixture
def job_count(request) -> int:
    return int(request.config.getoption("--jobs"))


@pytest.fixture
def single_use(request) -> bool:
    return bool(request.config.getoption("--single-use"))


@pytest.fixture
def run_delay(request) -> int:
    return int(request.config.getoption("--run-delay"))


@pytest.fixture
def cpu_quota(request) -> float:
    return float(request.config.getoption("--cpu-quota"))


@pytest.fixture
def memory_quota(request) -> float:
    return float(request.config.getoption("--memory-quota"))


@pytest.fixture
def work_duration(request) -> int:
    return int(request.config.getoption("--work-duration"))


@pytest.fixture
def mom(request) -> str:
    return request.config.getoption("--mom")


@pytest.fixture
def scenario(request) -> str:
    return request.config.getoption("--scenario")


@pytest.fixture
def external_volume(request) -> bool:
    return bool(request.config.getoption("--external-volume"))


@pytest.fixture
def min_index(request) -> int:
    return int(request.config.getoption("--min"))


@pytest.fixture
def max_index(request) -> int:
    return int(request.config.getoption("--max"))


@pytest.fixture
def batch_size(request) -> int:
    return int(request.config.getoption("--batch-size"))


@pytest.fixture
def service_id_list(request) -> str:
    return request.config.getoption("--service-ids")


@pytest.fixture
def enforce_quota_guarantee(request) -> bool:
    return request.config.getoption("--enforce-quota-guarantee")


@pytest.fixture
def enforce_quota_limit(request) -> bool:
    return request.config.getoption("--enforce-quota-limit")

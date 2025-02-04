import pytest

from xcrypt_python.job import Job
from xcrypt_python.scheduler import JobScheduler


@pytest.fixture
def scheduler_config():
    return {"max_jobs": 5}


@pytest.fixture
def job_config():
    return {
        "name": "test_job",
        "command": "echo 'Hello, World!'",
        "schedule": "0 0 * * *",
    }


def test_scheduler_initialization(scheduler_config):
    scheduler = JobScheduler(scheduler_config)
    assert scheduler.scheduler_config["max_jobs"] == 5
    assert len(scheduler.jobs) == 0


def test_scheduler_schedule_job(scheduler_config, job_config):
    scheduler = JobScheduler(scheduler_config)
    job = Job(job_config)
    scheduler.schedule(job)
    assert len(scheduler.jobs) == 1
    assert scheduler.jobs[0].name == "test_job"


def test_scheduler_run(scheduler_config, job_config):
    scheduler = JobScheduler(scheduler_config)
    job = Job(job_config)
    scheduler.schedule(job)
    scheduler.run()
    # Here you would implement the logic to test the run method
    # For now, we'll just call it to ensure it doesn't raise an exception
    scheduler.run()

import pytest

from xcrypt_python.job import Job


@pytest.fixture
def job_config():
    return {
        "name": "test_job",
        "command": "echo 'Hello, World!'",
        "schedule": "0 0 * * *",
    }


def test_job_initialization(job_config):
    job = Job(job_config)
    assert job.name == "test_job"
    assert job.command == "echo 'Hello, World!'"
    assert job.schedule == "0 0 * * *"


def test_job_run(job_config):
    job = Job(job_config)
    # Here you would implement the logic to test the run method
    # For now, we'll just call it to ensure it doesn't raise an exception
    job.run()

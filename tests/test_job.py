import pytest
from xcrypt_python.job import Job
import subprocess

@pytest.fixture
def job_config():
    return {
        "name": "test_job",
        "command": "echo 'Hello, World!'",
        "schedule": "0 0 * * *"
    }

def test_job_initialization(job_config):
    job = Job(job_config)
    assert job.name == "test_job"
    assert job.command == "echo 'Hello, World!'"
    assert job.schedule == "0 0 * * *"

def test_job_run(job_config):
    job = Job(job_config)
    result = subprocess.run(job.command, shell=True, capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, World!"
    job.run()

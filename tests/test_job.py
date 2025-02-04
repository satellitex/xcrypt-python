import pytest
from xcrypt_python.job import Job

def test_job_initialization():
    job = Job(job_id=1, job_name="Test Job", job_data={})
    assert job.job_id == 1
    assert job.job_name == "Test Job"
    assert job.job_data == {}
    assert job.status == "pending"

def test_job_schedule():
    job = Job(job_id=1, job_name="Test Job", job_data={})
    job.schedule()
    assert job.status == "scheduled"

def test_job_execute():
    job = Job(job_id=1, job_name="Test Job", job_data={})
    job.execute()
    assert job.status == "completed"

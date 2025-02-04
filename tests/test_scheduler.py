import pytest
from xcrypt_python.scheduler import JobScheduler
from xcrypt_python.job import Job

def test_add_job():
    scheduler = JobScheduler()
    job = Job(job_id=1, job_name="Test Job", job_data={})
    scheduler.add_job(job)
    assert len(scheduler.jobs) == 1
    assert scheduler.jobs[0].job_id == 1

def test_remove_job():
    scheduler = JobScheduler()
    job1 = Job(job_id=1, job_name="Test Job 1", job_data={})
    job2 = Job(job_id=2, job_name="Test Job 2", job_data={})
    scheduler.add_job(job1)
    scheduler.add_job(job2)
    scheduler.remove_job(1)
    assert len(scheduler.jobs) == 1
    assert scheduler.jobs[0].job_id == 2

def test_execute_jobs():
    scheduler = JobScheduler()
    job1 = Job(job_id=1, job_name="Test Job 1", job_data={})
    job2 = Job(job_id=2, job_name="Test Job 2", job_data={})
    scheduler.add_job(job1)
    scheduler.add_job(job2)
    scheduler.execute_jobs()
    assert job1.status == "completed"
    assert job2.status == "completed"

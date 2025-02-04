from xcrypt_python.job import Job
from xcrypt_python.scheduler import JobScheduler

# Create a job
job1 = Job(job_id=1, job_name="Example Job", job_data={"param1": "value1"})

# Create a scheduler
scheduler = JobScheduler()

# Add job to scheduler
scheduler.add_job(job1)

# Execute jobs in scheduler
scheduler.execute_jobs()

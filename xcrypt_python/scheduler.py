class JobScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)
        print(f"Job {job.job_name} added to the scheduler.")

    def remove_job(self, job_id):
        self.jobs = [job for job in self.jobs if job.job_id != job_id]
        print(f"Job with ID {job_id} removed from the scheduler.")

    def execute_jobs(self):
        for job in self.jobs:
            job.execute()

class Job:
    def __init__(self, job_id, job_name, job_data):
        self.job_id = job_id
        self.job_name = job_name
        self.job_data = job_data
        self.status = "pending"

    def schedule(self):
        self.status = "scheduled"
        print(f"Job {self.job_name} scheduled.")

    def execute(self):
        self.status = "running"
        print(f"Job {self.job_name} is running.")
        # Simulate job execution
        self.status = "completed"
        print(f"Job {self.job_name} completed.")

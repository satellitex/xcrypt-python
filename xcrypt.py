# xcrypt_python_implementation
# Python implementation of the Xcrypt parallel job scheduling tool.

import os
import subprocess
from typing import List, Dict

class Xcrypt:
    def __init__(self):
        self.jobs = []
        self.history = []

    def add_job(self, job_id: str, command: str, resources: Dict):
        job = {
            "id": job_id,
            "command": command,
            "resources": resources,
            "status": "initialized",
        }
        self.jobs.append(job)

    def execute_job(self, job_id: str):
        for job in self.jobs:
            if job["id"] == job_id:
                try:
                    job["status"] = "running"
                    result = subprocess.run(job["command"], shell=True, capture_output=True)
                    job["status"] = "done" if result.returncode == 0 else "failed"
                    self.history.append(job)
                    print(f"Job {job_id} execution completed with status: {job['status']}.")
                except Exception as e:
                    print(f"Error executing job {job_id}: {e}")
                break

    def cancel_job(self, job_id: str):
        for job in self.jobs:
            if job["id"] == job_id:
                job["status"] = "cancelled"
                print(f"Job {job_id} has been cancelled.")
                break

    def list_jobs(self):
        return [
            {"id": job["id"], "status": job["status"]} for job in self.jobs
        ]

    def list_history(self):
        return self.history

# Example Usage
if __name__ == "__main__":
    xcrypt = Xcrypt()

    # Add jobs
    xcrypt.add_job("job1", "echo 'Hello from Job 1'", {"cores": 2, "memory": "4G"})
    xcrypt.add_job("job2", "echo 'Hello from Job 2'", {"cores": 4, "memory": "8G"})

    # Execute jobs
    xcrypt.execute_job("job1")
    xcrypt.execute_job("job2")

    # Cancel a job
    xcrypt.cancel_job("job1")

    # List jobs
    print("Current Jobs:", xcrypt.list_jobs())

    # List history
    print("Execution History:", xcrypt.list_history())

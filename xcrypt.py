# xcrypt_python_implementation
# Python implementation of the Xcrypt parallel job scheduling tool.

import os
import subprocess
from typing import List, Dict

class Xcrypt:
    def __init__(self):
        self.jobs = []
        self.history = []
        self.dependencies = {}
        self.limits = {"max_jobs": None, "current_jobs": 0}

    def add_job(self, job_id: str, command: str, resources: Dict, dependencies: List[str] = None):
        job = {
            "id": job_id,
            "command": command,
            "resources": resources,
            "status": "initialized",
            "dependencies": dependencies or [],
        }
        self.jobs.append(job)
        if dependencies:
            self.dependencies[job_id] = dependencies

    def execute_job(self, job_id: str):
        for job in self.jobs:
            if job["id"] == job_id:
                if self.limits["max_jobs"] and self.limits["current_jobs"] >= self.limits["max_jobs"]:
                    print(f"Job {job_id} cannot be executed due to job limit.")
                    return

                if job["dependencies"]:
                    for dep in job["dependencies"]:
                        dep_job = next((j for j in self.jobs if j["id"] == dep), None)
                        if dep_job and dep_job["status"] != "done":
                            print(f"Job {job_id} cannot be executed until dependency {dep} is done.")
                            return

                try:
                    job["status"] = "running"
                    self.limits["current_jobs"] += 1
                    result = subprocess.run(job["command"], shell=True, capture_output=True)
                    job["status"] = "done" if result.returncode == 0 else "failed"
                    self.limits["current_jobs"] -= 1
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

    def set_job_limit(self, max_jobs: int):
        self.limits["max_jobs"] = max_jobs

    def create_sandbox(self, job_id: str):
        sandbox_dir = os.path.join(os.getcwd(), f"sandbox_{job_id}")
        os.makedirs(sandbox_dir, exist_ok=True)
        return sandbox_dir

    def execute_job_in_sandbox(self, job_id: str):
        for job in self.jobs:
            if job["id"] == job_id:
                sandbox_dir = self.create_sandbox(job_id)
                try:
                    job["status"] = "running"
                    self.limits["current_jobs"] += 1
                    result = subprocess.run(job["command"], shell=True, cwd=sandbox_dir, capture_output=True)
                    job["status"] = "done" if result.returncode == 0 else "failed"
                    self.limits["current_jobs"] -= 1
                    self.history.append(job)
                    print(f"Job {job_id} execution completed with status: {job['status']}.")
                except Exception as e:
                    print(f"Error executing job {job_id} in sandbox: {e}")
                break

    def generate_dynamic_jobs(self, base_command: str, param_ranges: Dict[str, List]):
        from itertools import product
        param_keys = list(param_ranges.keys())
        param_values = list(param_ranges.values())
        for param_combination in product(*param_values):
            job_id = f"job-{'-'.join(map(str, param_combination))}"
            command = base_command.format(**dict(zip(param_keys, param_combination)))
            self.add_job(job_id, command, {})

    def execute_jobs_parallel(self):
        import threading
        threads = []
        for job in self.jobs:
            if job["status"] == "initialized":
                thread = threading.Thread(target=self.execute_job, args=(job["id"],))
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.join()

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

    # Set job limit
    xcrypt.set_job_limit(2)

    # Add job with dependencies
    xcrypt.add_job("job3", "echo 'Hello from Job 3'", {"cores": 2, "memory": "4G"}, dependencies=["job1", "job2"])

    # Execute job with dependencies
    xcrypt.execute_job("job3")

    # Execute job in sandbox
    xcrypt.execute_job_in_sandbox("job3")

    # Generate dynamic jobs
    xcrypt.generate_dynamic_jobs("echo 'Hello from Job {param1}-{param2}'", {"param1": [1, 2], "param2": ["A", "B"]})

    # Execute jobs in parallel
    xcrypt.execute_jobs_parallel()

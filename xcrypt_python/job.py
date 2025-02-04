import subprocess

class Job:
    def __init__(self, job_config):
        self.name = job_config.get("name")
        self.command = job_config.get("command")
        self.schedule = job_config.get("schedule")

    def run(self):
        result = subprocess.run(self.command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Job {self.name} executed successfully")
        else:
            print(f"Job {self.name} failed with error: {result.stderr}")

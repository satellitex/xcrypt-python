import yaml


class Config:
    def __init__(self, config_file):
        with open(config_file, "r") as file:
            self.config = yaml.safe_load(file)
        self.log_level = self.config.get("log_level", "INFO")
        self.scheduler = self.config.get("scheduler", {})
        self.jobs = self.config.get("jobs", [])

    def get_job_config(self, job_name):
        for job in self.jobs:
            if job.get("name") == job_name:
                return job
        return None

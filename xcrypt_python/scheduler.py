class JobScheduler:
    def __init__(self, scheduler_config):
        self.scheduler_config = scheduler_config
        self.jobs = []

    def schedule(self, job):
        self.jobs.append(job)

    def run(self):
        for job in self.jobs:
            job.run()

import click
from xcrypt_python.job import Job
from xcrypt_python.scheduler import JobScheduler
from xcrypt_python.config import Config
from xcrypt_python.utils import setup_logging

@click.group()
def main():
    """Xcrypt-Python CLI"""
    pass

@main.command()
@click.argument('config_file', type=click.Path(exists=True))
def run(config_file):
    """Run jobs based on the configuration file"""
    config = Config(config_file)
    setup_logging(config.log_level)
    scheduler = JobScheduler(config.scheduler)
    jobs = [Job(job_config) for job_config in config.jobs]
    for job in jobs:
        scheduler.schedule(job)
    scheduler.run()

if __name__ == "__main__":
    main()

import click
from xcrypt_python.config import Config
from xcrypt_python.job import Job
from xcrypt_python.scheduler import JobScheduler
from xcrypt_python.utils import setup_logging


@click.command()
@click.option(
    "--config", default="example2.yaml", help="Path to the configuration file."
)
def main(config):
    # Load configuration
    config = Config(config)

    # Setup logging
    logger = setup_logging(config.log_level)

    # Initialize scheduler
    scheduler = JobScheduler(config.scheduler)

    # Add jobs to scheduler
    for job_config in config.jobs:
        job = Job(job_config)
        scheduler.schedule(job)

    # Run scheduler
    scheduler.run()


if __name__ == "__main__":
    main()

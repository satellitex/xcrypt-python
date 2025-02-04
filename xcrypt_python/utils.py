import logging


def setup_logging(log_level):
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    return logger


def validate_config(config):
    required_keys = ["log_level", "scheduler", "jobs"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    return True

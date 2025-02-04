# Xcrypt-Python Architecture

## Overview
Xcrypt-Python is a job scheduling and management system designed to handle parallel job execution. The system is built using Python and leverages various libraries to provide a robust and flexible solution for job scheduling.

## Components

### 1. CLI (`xcrypt_python/cli.py`)
The CLI is the entry point for interacting with the Xcrypt-Python system. It uses the `Click` library to provide a user-friendly command-line interface. The CLI allows users to run jobs based on a configuration file.

### 2. Job (`xcrypt_python/job.py`)
The `Job` class is responsible for defining and managing individual jobs. Each job has a name, command, and schedule. The `run` method is used to execute the job.

### 3. JobScheduler (`xcrypt_python/scheduler.py`)
The `JobScheduler` class is responsible for scheduling and running jobs. It maintains a list of jobs and provides methods to schedule and run them.

### 4. Config (`xcrypt_python/config.py`)
The `Config` class is responsible for loading and managing configuration settings from a YAML file. It provides methods to access various configuration options, such as log level, scheduler settings, and job definitions.

### 5. Utils (`xcrypt_python/utils.py`)
The `utils.py` file contains utility functions that are used throughout the system. These functions include logging setup and other common tasks.

## Workflow
1. The user interacts with the CLI to run jobs based on a configuration file.
2. The `Config` class loads the configuration settings from the specified YAML file.
3. The `JobScheduler` class schedules the jobs based on the configuration settings.
4. The `Job` class defines and manages individual jobs.
5. The `JobScheduler` class runs the scheduled jobs.

## Dependencies
- `Click`: Used for creating the CLI.
- `PyYAML`: Used for loading configuration settings from YAML files.
- `pytest`: Used for running tests.
- `rich`: Used for providing colored output in the CLI.
- `mypy`: Used for type checking.
- `black`: Used for code formatting.
- `flake8`: Used for linting.
- `isort`: Used for sorting imports.

## Directory Structure
```
Xcrypt-Python/
│── .github/
│   ├── workflows/
│   │   ├── ci.yml
│── xcrypt_python/
│   ├── __init__.py
│   ├── cli.py
│   ├── job.py
│   ├── scheduler.py
│   ├── config.py
│   ├── utils.py
│── tests/
│   ├── __init__.py
│   ├── test_job.py
│   ├── test_scheduler.py
│   ├── test_cli.py
│── scripts/
│   ├── setup_env.sh
│   ├── run_linter.sh
│── docs/
│   ├── index.md
│   ├── usage.md
│   ├── architecture.md
│── examples/
│   ├── example1.py
│   ├── example2.yaml
│── .gitignore
│── .pre-commit-config.yaml
│── pyproject.toml
│── poetry.lock
│── README.md
│── LICENSE
```

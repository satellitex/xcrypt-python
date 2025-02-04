# Usage Instructions

## Installation

To install Xcrypt-Python, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourname/Xcrypt-Python.git
   cd Xcrypt-Python
   ```

2. **Set up Poetry:**
   ```sh
   # Install Poetry
   pip install poetry

   # Create a virtual environment & install dependencies
   poetry install
   ```

## CLI Usage

Xcrypt-Python provides a command-line interface (CLI) for interacting with the system. The CLI allows you to run jobs based on a configuration file.

### Running Jobs

To run jobs based on a configuration file, use the `run` command:

```sh
poetry run xcrypt-python run <config_file>
```

Replace `<config_file>` with the path to your configuration file.

### Example Configuration File

Here is an example of a configuration file (`example.yaml`):

```yaml
log_level: INFO
scheduler:
  type: simple
jobs:
  - name: job1
    type: shell
    command: echo "Hello, World!"
  - name: job2
    type: shell
    command: echo "This is job 2"
```

### Checking CLI Help

To see the available commands and options, use the `--help` flag:

```sh
poetry run xcrypt-python --help
```

## Running Tests

To run the tests, use the following command:

```sh
poetry run pytest
```

## Linter & Formatter

To check the code formatting and run linters, use the following commands:

```sh
poetry run black .
poetry run mypy xcrypt_python/
poetry run flake8 xcrypt_python/ tests/
poetry run isort xcrypt_python/ tests/ --check-only
```

## Pre-commit Hooks

To set up pre-commit hooks, use the following command:

```sh
poetry run pre-commit install
```

This will ensure that the linters and formatters run automatically before each commit.

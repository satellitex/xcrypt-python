# Usage

## Installation

To install Xcrypt-Python, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourname/Xcrypt-Python.git
    cd Xcrypt-Python
    ```

2. Install Poetry:
    ```sh
    pip install poetry
    ```

3. Create a virtual environment and install dependencies:
    ```sh
    poetry install
    ```

## CLI Tool

Xcrypt-Python provides a command-line interface (CLI) for interacting with the system. The following commands are available:

- `start`: Start a job
- `stop`: Stop a job
- `status`: Check the status of a job

To use the CLI tool, run the following command:
```sh
poetry run xcrypt-python --help
```

## Running Tests

To run the tests, use the following command:
```sh
poetry run pytest
```

## Linter and Formatter

To check the code formatting and run linters, use the following commands:
```sh
poetry run black .
poetry run mypy xcrypt_python/
```

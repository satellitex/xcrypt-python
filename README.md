# Xcrypt-Python

Xcrypt-Python is a Python-based job scheduling and management system. It allows users to create, manage, and schedule jobs using a simple and intuitive interface. The system is designed to be flexible and extensible, making it suitable for a wide range of use cases.

## Features

- **Job Management**: Create, manage, and schedule jobs with ease.
- **CLI Interface**: Use the command-line interface to interact with the system.
- **Configuration Management**: Manage configuration files using YAML.
- **Extensible**: Easily extend the system to add new features and functionality.
- **Testing**: Comprehensive unit tests to ensure the system works as expected.

## Getting Started

To get started with Xcrypt-Python, follow the setup and development instructions provided in the documentation.

## Documentation

- [Usage](docs/usage.md): Instructions for installation and usage.
- [Architecture](docs/architecture.md): System design and architecture.

## Setup & Development

### 1. Clone the repository
```sh
git clone https://github.com/yourname/Xcrypt-Python.git
cd Xcrypt-Python
```

### 2. Poetry setup
```sh
# Install Poetry
pip install poetry

# Create virtual environment & install dependencies
poetry install
```

### 3. Verify CLI tool
```sh
poetry run xcrypt-python --help
```

### 4. Run tests
```sh
poetry run pytest
```

### 5. Linter & format check
```sh
poetry run black .
poetry run mypy xcrypt_python/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

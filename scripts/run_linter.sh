#!/bin/bash

# Run flake8 for linting
poetry run flake8 xcrypt_python/ tests/

# Run black for code formatting
poetry run black xcrypt_python/ tests/ --check

# Run isort for import sorting
poetry run isort xcrypt_python/ tests/ --check-only

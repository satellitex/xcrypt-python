#!/bin/bash

# Run flake8
poetry run flake8 xcrypt_python/ tests/

# Run black
poetry run black xcrypt_python/ tests/ --check

# Run isort
poetry run isort xcrypt_python/ tests/ --check-only

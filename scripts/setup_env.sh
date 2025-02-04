#!/bin/bash

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install project dependencies
poetry install

# Verify installation
poetry --version
python3 --version

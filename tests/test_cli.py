import pytest
from click.testing import CliRunner
from xcrypt_python.cli import main

def test_start():
    runner = CliRunner()
    result = runner.invoke(main, ['start'])
    assert result.exit_code == 0
    assert 'Starting a job...' in result.output

def test_stop():
    runner = CliRunner()
    result = runner.invoke(main, ['stop'])
    assert result.exit_code == 0
    assert 'Stopping a job...' in result.output

def test_status():
    runner = CliRunner()
    result = runner.invoke(main, ['status'])
    assert result.exit_code == 0
    assert 'Checking job status...' in result.output

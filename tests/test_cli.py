import pytest
from click.testing import CliRunner
from xcrypt_python.cli import main

def test_run_command():
    runner = CliRunner()
    result = runner.invoke(main, ['run', 'tests/test_config.yaml'])
    try:
        assert result.exit_code == 0
        assert "Job scheduled" in result.output
    except SystemExit as e:
        assert e.code == 0

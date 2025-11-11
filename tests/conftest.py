import pytest
import subprocess
import sys

# This runs the equivalent of `uv pip install -e .` at the start of the session so that uv registers the entrypoint `PMC_id_convert` for the script as a command that can be called on the command line
'''
During development (now):
I need `uv pip install -e .` in tests because the CLI entry point isn't registered yet.
After publishing to PyPI:
Users will have already done pip install PMC-ID-Converter-for-humans, so the PMC_id_convert command is already available. No installation needed in tests.
'''
#SO I ADDED testing and skipping the `uv pip install -e .` if `pip install` of the packge already somehow or other occured. 
@pytest.fixture(scope="session", autouse=True)
def ensure_package_installed():
    """Ensure package is installed (for CLI tests to work)."""
    try:
        # Check if CLI command exists
        subprocess.run(['PMC_id_convert', '--help'], 
                      capture_output=True, 
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Not installed, install in editable mode (dev only)
        subprocess.run(['uv', 'pip', 'install', '-e', '.'], 
                      check=True, 
                      capture_output=True)
    yield
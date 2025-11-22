import pytest
import subprocess
import sys
import importlib

# This runs the equivalent of `uv pip install -e .` at the start of the session so that uv registers the entrypoint `PMC_id_convert` for the script as a command that can be called on the command line
'''
During development (now):
I needed `uv pip install -e .` at the start of test pahse because the CLI entry point wassn't registered yet.
After using `pip install git+https://github.com/fomightez/PubMed_Central_ID_Converter_for_humans.git` to install the current github version or publishing to PyPI(or TestPyPI) and then users using `pip install`:
MyBinder session that comes (or users local use) will have already done `pip install` PMC-ID-Converter-for-humans (or equivalent), so the PMC_id_convert command is already available. No installation needed in tests.
However, I left a way in the notebook `test_the_package.ipynb` to add running `uv pip install -e .` again to use the current in-session code for the package by setting
`use_freshest_in_session_package_code` to `True`. This leaves a way to actively test
what is changed in the session instead of just testing what was `pip` installed, 
which is the default for now.
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
        
        # CRITICAL: Invalidate import caches so Python knows about the new package
        importlib.invalidate_caches()
        
        # Also ensure the package location is in sys.path
        import site
        importlib.reload(site)
    
    yield
    # Note that without the `importlib.invalidate_caches()` if I start the MyBinder served session, it doesn't find the module and I found if I opened the test file and saved it without changing ANYTHING, it changed the time stamp and pytest imported it again and it worked. `importlib.invalidate_caches()` tells Python to forget what it thought it knew about what packages are available. This forces Python to rescan the filesystem when the import statement is encountered, and without my needing to save it manually to trigger it.
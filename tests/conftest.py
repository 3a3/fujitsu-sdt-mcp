"""
Test configuration file
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root directory to PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup test environment variables
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up environment variables for testing"""
    os.environ["FUJITSU_API_BASE_URL"] = "https://test-api.example.com/sdtp"
    os.environ["FUJITSU_API_KEY"] = "test-api-key"
    
    yield
    
    # Clean up after tests
    if "FUJITSU_API_BASE_URL" in os.environ:
        del os.environ["FUJITSU_API_BASE_URL"]
    if "FUJITSU_API_KEY" in os.environ:
        del os.environ["FUJITSU_API_KEY"]

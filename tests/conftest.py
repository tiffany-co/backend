"""
This is the main configuration file for pytest.

It can be used to define fixtures, hooks, and plugins that are shared across all test files.
Fixtures defined here have a global scope.

For now, this file is kept simple, but it will be crucial for setting up
test database sessions and API clients as we build out integration and API tests.
"""
import sys
from pathlib import Path

# --- Add project root to Python path ---
# This ensures that pytest can find and import the 'app' module correctly.
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

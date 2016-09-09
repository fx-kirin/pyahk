""" Test runner

Preforms path mangling magic required to run test.
"""
import unittest
import os, sys

cwd = os.getcwd()
# Append the inner package folder to the path so test can access internals
sys.path.append(os.path.join(cwd, 'ahk'))

# Gather tests
from test import all_tests

# Run tests
unittest.TextTestRunner(verbosity=2).run(all_tests)

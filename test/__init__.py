"""Bundle tests as a module."""
import unittest
import test_ahk, test_script, test_control

# Gather all sub-tests into one suite
all_tests = unittest.TestSuite([
                                test_ahk.all_tests,
                                test_script.all_tests,
                                test_control.all_tests,
                               ])

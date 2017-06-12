# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

"""Bundle tests as a module."""
import unittest
import test.ahk, test.script, test.control

# Gather all sub-tests into one suite
all_tests = unittest.TestSuite([
    test.ahk.all_tests,
    test.script.all_tests,
    test.control.all_tests,
])

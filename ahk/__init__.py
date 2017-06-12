# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

"""OO wrappers around the AutoHotKey library.

This package provides both direct access to wrapped versions of the functions
provided by the ahkdll, and also object wrappers around common operations.
"""
from ahk.ahk import *
from ahk.script import Function, Script
from ahk.control import Control

__version__ = "0.3.0"


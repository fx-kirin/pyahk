# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

from ahk import ahk

ahk.start()
ahk.ready()
ahk.execute(u"something = 10")
ahk.get(u"something")
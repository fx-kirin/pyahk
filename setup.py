# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals

from setuptools import setup

import ahk

setup(name='pyahk',
      version=ahk.__version__,
      author='Ed Blake',
      author_email='kitsu.eb@gmail.com',
      url='https://bitbucket.org/kitsu/pyahk',
      description='AutoHotKey.dll wrapped by ctypes.',
      long_description=ahk.__doc__,
      license="Modified BSD",
      packages=['ahk'],
      data_files=[('', 
                   ['README.rst',
                    'LICENSE_AutoHotkey.txt',
					'LICENSE_pyahk.txt',
                    'runtests.py'
                   ])],
      keywords=['Windows','Automation','AutoHotKey'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
		  'Programming Language :: Python :: 3',
		  'Programming Language :: Python :: 3.3',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ],
)

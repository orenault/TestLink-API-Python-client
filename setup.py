#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012 ??? , ???
#
#  Licensed under ???
#  

from os.path import join, dirname
from distutils.core import setup

execfile(join(dirname(__file__), 'src', 'testlink', 'version.py'))

setup(name='TestLink',
      version=VERSION,
      description='Python XMLRPC client for the TestLink API',
      author='James Stock, Olivier Renault, TestLink-API-Python-client developers',
      author_email='???, ???, ???',
      url='https://github.com/lczub/TestLink-API-Python-client',
      license      = 'unknown',
      package_dir  = {'': 'src'},
      packages=['testlink'],
     )


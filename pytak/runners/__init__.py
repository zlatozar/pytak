# -*- coding: utf-8 -*-

"""
.. module:: pytak.scenarios.runners
   :synopsis: Contains various types of runners

.. moduleauthor:: Zlatozar Zhelyazkov <zlatozar@gmail.com>

Runners change the environment as adding returned data in stack
"""

from runners import basic_login
from runners import xauth_login

# Types of runners
from runners import trace
from runners import run
from runners import run_function
from runners import perf
from runners import test

from runners import parallel

# Selector
from runners import select

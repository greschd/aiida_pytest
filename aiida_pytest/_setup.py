#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiida.cmdline.verdilib import setup as _setup
from aiida.cmdline.verdilib import Profile

from ._chainmap import ChainMap

def run_setup(**kwargs):
    defaults = {
        'backend': 'django',
        'email': 'aiida@localhost',
        'first_name': 'Test',
        'last_name': 'User',
        'institution': 'Test Lab',
        'non_interactive': True,
        'only_config': False,
        'db_host': 'localhost'
    }

    _setup(**ChainMap(kwargs, defaults))
    Profile().profile_setdefault(kwargs['profile'])

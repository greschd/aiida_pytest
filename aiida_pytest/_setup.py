#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiida.cmdline.verdilib import setup as _setup

from ._chainmap import ChainMap

def run_setup(repo_default, **kwargs):
    defaults = {
        'backend': 'django',
        'email': 'aiida@localhost',
        'first_name': 'Test',
        'last_name': 'User',
        'institution': 'Test Lab',
        'non_interactive': True,
        'only_config': False,
        'db_host': 'localhost',
        'db_port': '5432',
        'repo': repo_default
    }

    _setup(**ChainMap(kwargs, defaults))

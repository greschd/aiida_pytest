#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import pytest

__all__ = ['load_config']

@pytest.fixture(scope='session')
def load_config(aiidadb, setup_code):
    def inner(config_file):
        with open(config_file, 'r') as f:
            res = yaml.load(f)
        print(res)
        for code_kwargs in res['code']:
            setup_code(**code_kwargs)
    return  inner

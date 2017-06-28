#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def test_ls(setup_code):
    from aiida.orm.code import Code
    setup_code(
        label='ls',
        description='ls',
        local=False,
        default_plugin='simpleplugins.templatereplacer',
        remote_computer='localhost',
        remote_abspath='/bin/ls'
    )
    code = Code.get_from_string('ls')
    assert code.is_stored

def test_from_config(load_config):
    from aiida.orm.code import Code
    load_config(os.path.abspath('code_config.yml'))
    code = Code.get_from_string('echo')
    assert code.is_stored

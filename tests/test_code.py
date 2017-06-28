#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

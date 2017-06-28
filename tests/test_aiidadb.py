#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_aiidadb_loads(aiidadb):
    pass

def test_localhost_configured(aiidadb):
    from aiida.orm.computer import Computer
    from aiida.orm.user import User

    computer = Computer.get('localhost')
    assert computer.is_user_configured(User.get_all_users()[0])

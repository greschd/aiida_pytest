#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import aiida

def test_configure_from_file(configure_from_file):
    configure_from_file(os.path.abspath('config.yml'))
    from aiida.orm.user import User
    user = User.get_all_users()[0]
    assert user.first_name == 'AiiDA'

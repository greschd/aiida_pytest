#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import time

import aiida
from aiida.cmdline.commands.daemon import status
import pytest
from click.testing import CliRunner

from aiida_pytest.contextmanagers import redirect_stdout

def test_configure_from_file(configure):
    from aiida.orm.user import User
    user = User.get_all_users()[0]
    assert user.first_name == 'AiiDA'

def test_db_flushed(configure):
    from aiida.orm.data.base import Str
    test_string = 'this string should not be present when the test run starts'
    tag = 'Test string tag'
    from aiida.orm.querybuilder import QueryBuilder
    qb = QueryBuilder()
    qb.append(
        Str,
        filters={'label': {'==': tag}}
    )
    assert not qb.all()
    str_obj = Str(test_string)
    str_obj.label = tag
    str_obj.store()

def test_daemon_running(configure_with_daemon):
    from aiida.cmdline.verdilib import Daemon
    start_time = time.time()
    max_timeout = 5
    runner = CliRunner()
    while time.time() - start_time < max_timeout:
        res = runner.invoke(status)
        if 'Daemon is running as PID' in res.output:
            break
    else:
        raise ValueError('Daemon not running after {} seconds. Status: {}'.format(max_timeout, res.output))

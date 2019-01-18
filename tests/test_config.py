#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import time

from click.testing import CliRunner
import aiida
from aiida.cmdline.commands.cmd_daemon import status


def test_configure_from_file(configure):
    from aiida.orm import QueryBuilder
    from aiida.orm import User
    qb = QueryBuilder()
    qb.append(User)
    user = qb.first()[0]
    assert user.first_name == 'AiiDA'


def test_db_flushed(configure):
    from aiida.orm.data.base import Str
    test_string = 'this string should not be present when the test run starts'
    tag = 'Test string tag'
    from aiida.orm.querybuilder import QueryBuilder
    qb = QueryBuilder()
    qb.append(Str, filters={'label': {'==': tag}})
    assert not qb.all()
    str_obj = Str(test_string)
    str_obj.label = tag
    str_obj.store()


def test_daemon_running(configure_with_daemon):
    start_time = time.time()
    max_timeout = 5
    runner = CliRunner()
    while time.time() - start_time < max_timeout:
        res = runner.invoke(status, catch_exceptions=False)
        if 'Daemon is running as PID' in res.output:
            break
    else:
        raise ValueError(
            'Daemon not running after {} seconds. Status: {}'.format(
                max_timeout, res.output))

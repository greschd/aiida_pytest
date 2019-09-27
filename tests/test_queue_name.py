#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

def test_queue_name(get_queue_name_from_code):
    assert get_queue_name_from_code('ls') == 'test_queue_name'

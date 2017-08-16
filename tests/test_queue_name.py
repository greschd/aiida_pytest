#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_queue_name(get_queue_name_from_code):
    assert get_queue_name_from_code('ls') == 'test_queue_name'

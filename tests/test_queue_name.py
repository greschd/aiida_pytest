#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_queue_name(queue_name_from_code):
    assert queue_name_from_code('ls') == 'test_queue_name'

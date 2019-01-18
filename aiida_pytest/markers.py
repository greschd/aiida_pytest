# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import pytest

try:
    from aiida.common import caching
    HAS_CACHING = True
except ImportError:
    HAS_CACHING = False

__all__ = ['skip_caching']

skip_caching = pytest.mark.skipif(
    not HAS_CACHING,
    reason='The AiiDA version does not support caching.'
)

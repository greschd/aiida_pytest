import aiida
import pytest

skip_caching = pytest.mark.skipif(
    hasattr(aiida.common, 'caching'),
    reason='The AiiDA version does not support caching.'
)

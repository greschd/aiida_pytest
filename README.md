# aiida-pytest

This is a helper to enable testing AiiDA plugins with ``pytest``. The main purpose is to create a fixture which sets up a temporary AiiDA database and user, and simplify setting up the computers and calculations.

To get started, create a ``tests`` folder where your ``pytest`` tests will be located. In ``conftests.py``, you need to write

```python
from aiida_pytest import *
```

This defines the ``config`` fixture.

Also, you need to create an empty ``.aiida`` in the folder where you want to run your tests. Then, you need to ``export AIIDA_PATH='.'`` to make sure aiida is using this config folder. This is to make sure that the tests create a local configuration (that will be destroyed after the test) instead of running in your main AiiDA configuration.

## Installation: pgtest

Currently, the version of ``pgtest`` available on PyPI does not work with ``aiida-pytest``. For this reason, you must install it with ``pip install -r requirements.txt``, using the provided requirements file.

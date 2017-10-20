# aiida-pytest

This is a helper to enable testing AiiDA plugins with ``pytest``. The main purpose is to create a fixture which sets up a temporary AiiDA database and user, and simplify setting up the computers and calculations.

To get started, create a ``tests`` folder where your ``pytest`` tests will be located. In ``conftests.py``, you need to write

```python
from aiida_pytest import *
```

This defines the ``configure`` and ``configure_with_daemon`` fixtures.

Also, you need to create an empty ``.aiida`` in the folder where you want to run your tests. Then, you need to ``export AIIDA_PATH='.'`` to make sure aiida is using this config folder. This is to make sure that the tests create a local configuration (that will be destroyed after the test) instead of running in your main AiiDA configuration.

**Note:** ``aiida-pytest`` is not compatible with the ``aiida-xdist`` plugin, since the fixtures with ``scope=session`` are then called for each running worker.

## Defining and running tests

Tests with ``aiida-pytest`` are defined and run exactly like "regular" ``pytest`` tests. If a test needs the AiiDA database, it should use the ``configure`` fixture. If the test also requires the Daemon to run, it should use the ``configure_with_daemon`` fixture. Note that, since certain AiiDA import statements require the database backend to be set, these imports should be done **inside** the test function.

After the tests have run, the code will wait for you to press ``Enter`` before deleting the testing database and repository. This gives you the opportunity to manually inspect the final state. If you want to avoid this step (for example in a CI system), pass the ``--quiet-wipe`` flag to ``py.test``.

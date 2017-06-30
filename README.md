# aiida-pytest

This is a helper to enable testing AiiDA plugins with ``pytest``. The main purpose is to create a fixture which sets up a temporary AiiDA database and user, and simplify setting up the computers and calculations.

To get started, create a ``tests`` folder where your ``pytest`` tests will be located. In ``conftests.py``, you need to write

```python
from aiida_pytest import *
```

This defines the ``config`` fixture.

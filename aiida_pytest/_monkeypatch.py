import pytest
from fsc.export import export

@export
@pytest.fixture
def submit_as_async(monkeypatch):
    import aiida.work
    monkeypatch.setattr(aiida.work, 'submit', aiida.work.async)

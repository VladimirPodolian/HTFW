import pytest
from src.rest.api import Api


@pytest.fixture()
def api():
    return Api()

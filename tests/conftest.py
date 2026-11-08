import pytest
from fastapi.testclient import TestClient

from support_agent.api import app
from support_agent.graph import build_graph


@pytest.fixture
def graph():
    return build_graph()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

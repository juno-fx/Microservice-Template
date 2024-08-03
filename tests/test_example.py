"""
Tests for kuiper mounts
"""
# 3rd
from fastapi.testclient import TestClient

# local
from src import app

client = TestClient(app)


def test_utility_endpoint():
    """
    Test the utility endpoint
    """
    response = client.get("/.health")
    assert response.status_code == 200


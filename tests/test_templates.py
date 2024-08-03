"""
Tests for kuiper workstation templates
"""
# 3rd
from pytest import raises
from fastapi.testclient import TestClient

# local
from pprint import pprint
from kuiper import app

client = TestClient(app)


def test_workstation_templates():
    """
    Test that we can create a shared workstation
    """
    response = client.get("/kuiper/config/workstation/schema")
    assert response.status_code == 200
    assert len(response.json()) != 0


def test_create_workstation_templates():
    """
    Test that we can assign a mount
    """
    response = client.post(
        "/kuiper/config/workstation",
        json={
            "registry": "registry.hatfieldfx.com",
            "icon": "https://cdn-icons-png.flaticon.com/512/3515/3515293.png",
            "label": "Artist tom; ::: /123/ Machine v2",
            "repo": "string",
            "tag": "string",
            "cpu": "1500m",
            "memory": "1Gi",
            "gpu": False,
            "group": "string"
        }
    )
    assert response.status_code == 200
    assert len(response.json()) != 0

    response = client.get("/kuiper/catalog")
    assert response.status_code == 200
    for item in response.json():
        if item['label'] == 'Artist tom 123 Machine v2':
            break
    else:
        raise Exception("Failed to find template in catalog")

    for item in response.json():
        if item['label'] == 'Artist tom 123 Machine v2':
            response = client.delete(f"/kuiper/config/workstation/{item['label']}")
            assert response.status_code == 200

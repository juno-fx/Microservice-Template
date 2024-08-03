"""
Tests for kuiper mounts
"""
# 3rd
from pytest import raises
from fastapi.testclient import TestClient

# local
from pprint import pprint
from kuiper import app

client = TestClient(app)


def test_volumes():
    """
    Test that we can create a shared workstation
    """
    response = client.get("/kuiper/config/volumes")
    assert response.status_code == 200
    assert len(response.json()) != 0


def test_assign_mount():
    """
    Test that we can assign a mount
    """
    response = client.get("/kuiper/config/volumes")
    assert response.status_code == 200
    assert len(response.json()) != 0

    target = response.json()[0]

    # verify we have no volumes
    response = client.get("/kuiper/config/mount")
    for volume in response.json():
        response = client.delete(f"/kuiper/config/mount/{volume['volume']}")
        assert response.status_code == 200

    response = client.get("/kuiper/config/mount")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.post(
        "/kuiper/config/mount",
        json={
            "volume": target,
            "sub_path": "none",
            "container_path": "/test",
        }
    )
    assert response.status_code == 200
    assert response.json()['volume'] == target

    # verify it was created
    response = client.get("/kuiper/config/mount")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.delete(f"/kuiper/config/mount/{target}")
    assert response.status_code == 200

    response = client.post(
        "/kuiper/config/mount",
        json={
            "volume": target,
            "container_path": "/test",
        }
    )
    assert response.status_code == 200
    assert response.json()['volume'] == target

    response = client.delete(f"/kuiper/config/mount/{target}")
    assert response.status_code == 200


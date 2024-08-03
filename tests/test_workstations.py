"""
Tests for kuiper
"""
# 3rd
from pytest import raises
from fastapi.testclient import TestClient

# local
from pprint import pprint
from kuiper import app

client = TestClient(app)


def test_access():
    """
    Verify that we can even use this endpoint
    """
    response = client.get("/kuiper/catalog")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create():
    """
    Test that we can create a workstation
    """
    response = client.get("/kuiper/catalog")
    assert response.status_code == 200
    raw_json = response.json()

    idx = None
    for option in raw_json:
        if option['label'] == 'Production':
            idx = option['idx']
            break

    response = client.get("/kuiper/config/volumes")
    assert response.status_code == 200
    assert len(response.json()) != 0

    target = response.json()[0]

    response = client.post(
        "/kuiper/config/mount",
        json={
            "volume": target,
            "sub_path": "/test",
            "container_path": "/test",
        }
    )
    assert response.status_code == 200
    assert response.json()['volume'] == target

    response = client.get(
        "/kuiper/test/request",
        params={"instance_type": idx}
    )
    assert response.status_code == 200


def test_get_one():
    """
    Test that we can get one workstation
    """
    response = client.get("/kuiper/test/describe")
    assert response.status_code == 200
    raw_json = response.json()
    assert len(raw_json) > 0

    workstation = raw_json[0]['name']

    response = client.get(f"/kuiper/test/describe/{workstation}")
    assert response.status_code == 200
    assert response.json()['name'] == workstation


def test_invalid_id():
    """
    Test that we handle invalid instance types
    """
    with raises(Exception) as exc_info:
        client.get(
            "/kuiper/test/request",
            params={"instance_type": "5"}
        )
    assert str(exc_info.value) == "Instance Type not found: 5"


def test_reboot():
    """
    Test that we can reboot a workstation
    """
    response = client.get("/kuiper/test/describe")
    assert response.status_code == 200
    raw_json = response.json()
    assert len(raw_json) > 0

    for workstation in raw_json:
        response = client.get(f"/kuiper/test/reboot/{workstation['name']}")
        assert response.status_code == 200


def test_list():
    """
    Test that we can list workstations
    """
    response = client.get("/kuiper/test/describe")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_all():
    """
    Test that we can get all workstations
    """
    response = client.get('/kuiper/all')
    assert response.status_code == 200
    raw_json = response.json()
    assert len(raw_json) > 0
    # block token distribution
    for instance in raw_json:
        assert 'token' not in instance


def test_delete():
    """
    Test that we can delete a workstation
    """
    response = client.get("/kuiper/test/describe")
    assert response.status_code == 200
    raw_json = response.json()
    assert len(raw_json) > 0

    for workstation in raw_json:
        response = client.get(f"/kuiper/test/shutdown/{workstation['name']}")
        assert response.status_code == 200

    response = client.get("/kuiper/test/describe")
    assert response.status_code == 200
    raw_json = response.json()
    assert len(raw_json) == 0


def test_set_shared():
    """
    Test that we can set a shared workstation
    """
    # Create a workstation
    test_create()

    # Get the workstation
    response = client.get("/kuiper/test/describe")
    assert response.status_code == 200
    raw_json = response.json()
    assert len(raw_json) > 0

    workstation = raw_json[0]

    # Set the shared workstation
    response = client.post(
        f"/kuiper/test/share/{workstation['name']}",
        json={"users": ["bob", "alice"]}
    )
    assert response.status_code == 200

    # Get the shared workstation
    response = client.get("/kuiper/bob/shared")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/kuiper/alice/shared")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Remove the shared workstation
    response = client.delete(f"/kuiper/test/share/{workstation['name']}")
    assert response.status_code == 200

    # Verify it has been deleted
    response = client.get("/kuiper/bob/shared")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.get("/kuiper/alice/shared")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_shared():
    """
    Test that we can create a shared workstation
    """
    response = client.get("/kuiper/test/shared")
    assert response.status_code == 200
    assert len(response.json()) == 0

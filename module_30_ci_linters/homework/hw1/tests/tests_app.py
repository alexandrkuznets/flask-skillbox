import pytest
from module_30_ci_linters.homework.hw1.main.models import Client, Parking
from module_30_ci_linters.homework.hw1.tests.factories import ClientFactory, ParkingFactory


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_get_req(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client):
    data = {"name": "Joe",
            "surname": "black",
            "credit_card": "111",
            "car_number": "AAA"}
    resp = client.post("/clients", query_string=data)

    assert resp.status_code == 201


def test_create_parking(client):
    data = {"address": "Street",
            "opened": True,
            "count_places": 10,
            "count_available_places": 10}
    resp = client.post("/parkings", query_string=data)

    assert resp.status_code == 201


@pytest.mark.parking
def test_create_client_parkings(client):
    data = {"client_id": 1,
            "parking_id": 1}
    resp = client.post("/client_parkings", query_string=data)

    assert resp.status_code == 201


@pytest.mark.parking
def test_delete_client_parkings(client):
    data = {"client_id": 2,
            "parking_id": 2}
    resp = client.delete("/client_parkings", query_string=data)

    assert resp.status_code == 201


def test_create_client_factories(app, db):
    client = ClientFactory()
    db.session.commit()
    assert len(db.session.query(Client).all()) == 2


def test_create_parking_factories(app, db):
    parking = ParkingFactory()
    db.session.commit()
    assert len(db.session.query(Parking).all()) == 2


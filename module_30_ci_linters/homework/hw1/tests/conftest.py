import datetime

import pytest
from module_30_ci_linters.homework.hw1.main.app import create_app, db as _db
from module_30_ci_linters.homework.hw1.main.models import Client, ClientParking, Parking
import werkzeug
werkzeug.__version__ = '2.0.3'

@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client = Client(id=1,
                        name="Joe",
                        surname="Black",
                        credit_card='1111',
                        car_number='AAA')
        parking = Parking(id=1,
                          address='New Street',
                          opened=True,
                          count_places=10,
                          count_available_places=10
                          )
        client_parking = ClientParking(id=2,
                                       client_id=2,
                                       parking_id=2,
                                       time_in=datetime.datetime.now()
                                       )
        _db.session.add(client_parking)
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db






import factory
import factory.fuzzy as fuzzy
import random

from ..main.app import db
from ..main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.Faker('credit_card_number')
    car_number = factory.Faker('text', max_nb_chars=10)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=10, max=100)
    count_available_places = factory.LazyAttribute(lambda o: random.randint(0, o.count_places))

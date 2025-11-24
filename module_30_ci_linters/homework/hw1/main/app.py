import datetime
from typing import Dict, List

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, ClientParking, Parking

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET", "POST"])
    def get_clients():
        if request.method == "GET":
            clients: List[Client] = db.session.query(Client).all()
            clients_list = [c.to_json() for c in clients]
            return jsonify(clients_list), 200

        elif request.method == "POST":
            name = request.args.get("name", type=str)
            surname = request.args.get("surname", type=str)
            credit_card = request.args.get("credit_card", type=str)
            car_number = request.args.get("car_number", type=str)

            new_client = Client(
                name=name,
                surname=surname,
                credit_card=credit_card,
                car_number=car_number,
            )

            db.session.add(new_client)
            db.session.commit()

            return "", 201

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client(client_id: int):
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route("/parkings", methods=["POST"])
    def create_parkings():
        address = request.args.get("address", type=str)
        count_places = request.args.get("count_places", type=int)

        new_parking = Parking(
            address=address,
            opened=True,
            count_places=count_places,
            count_available_places=count_places,
        )

        db.session.add(new_parking)
        db.session.commit()
        return "", 201

    @app.route("/client_parkings", methods=["POST", "DELETE"])
    def create_client_parkings():
        client_id = request.args.get("client_id", type=int)
        parking_id = request.args.get("parking_id", type=int)

        parking = db.session.query(Parking).get(parking_id)
        if request.method == "POST":
            if parking.opened and parking.count_available_places > 0:
                parking.count_available_places -= 1

                new_client_parking = ClientParking(
                    client_id=client_id,
                    parking_id=parking_id,
                    time_in=datetime.datetime.now(),
                )

                db.session.add(new_client_parking)
                db.session.commit()
                return "", 201
            return "The parking lot is closed or there are no free spaces", 200
        elif request.method == "DELETE":
            client_parkings = (
                db.session.query(ClientParking)
                .filter_by(parking_id=parking_id, client_id=client_id)
                .first()
            )
            client_parkings.time_out = datetime.datetime.now()
            db.session.commit()
            return "", 201

    return app


app = create_app()

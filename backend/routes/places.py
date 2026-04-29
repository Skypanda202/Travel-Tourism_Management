from flask import Blueprint, jsonify
from models import Place

places_bp = Blueprint("places", __name__)

@places_bp.route("/", methods=["GET"])
def get_places():
    places = Place.query.filter_by(district="Kalahandi").all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "description": p.description,
            "lat": p.latitude,
            "lng": p.longitude,
            "transport": p.transport,
            "qr": p.qr_code
        } for p in places
    ])
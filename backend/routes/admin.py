from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import db, Place
from utils.qr import generate_qr
import os

admin_bp = Blueprint("admin", __name__)

UPLOAD_FOLDER = "static/uploads"

# ------------------------
# LOGIN
# ------------------------
@admin_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if data["username"] == "admin" and data["password"] == "1234":
        token = create_access_token(identity="admin")
        return jsonify(access_token=token)

    return jsonify({"error": "Invalid credentials"}), 401


# ------------------------
# ADD PLACE (WITH IMAGE)
# ------------------------
@admin_bp.route("/add_place", methods=["POST"])
@jwt_required()
def add_place():

    # Get form data
    data = request.form

    # Handle image upload safely
    file = request.files.get("image")
    filename = None

    if file:
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    # Create place
    place = Place(
        name=data["name"],
        district=data["district"],
        category=data["category"],
        description=data["description"],
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        transport=data["transport"],
        image=filename
    )

    db.session.add(place)
    db.session.commit()

    # Generate QR
    qr_file = f"place_{place.id}.png"
    generate_qr(f"http://localhost:3000/place/{place.id}", qr_file)

    place.qr_code = qr_file
    db.session.commit()

    return jsonify({"message": "Place added successfully"})
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    district = db.Column(db.String(100))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    transport = db.Column(db.Text)
    qr_code = db.Column(db.String(200))
    image = db.Column(db.String(200))
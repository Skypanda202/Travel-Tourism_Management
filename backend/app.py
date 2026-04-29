from flask import Flask
from flask_cors import CORS
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tourism.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Import routes
from routes.places import places_bp
from routes.admin import admin_bp

app.register_blueprint(places_bp, url_prefix="/api/places")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Tourism Backend Running 🚀"

if __name__ == "__main__":
    app.run(debug=True)
    
# JWT AUTH

from flask_jwt_extended import JWTManager

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)
# app/__init__.py

from flask import Flask
from flask_pymongo import PyMongo
import os

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # Use environment variable for Mongo URI
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/cti_dashboard")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

    # Initialize Mongo
    mongo.init_app(app)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app


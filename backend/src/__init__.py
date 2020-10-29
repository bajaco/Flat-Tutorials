from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_LOCATION = os.environ.get('DATABASE_LOCATION')
    database_path = "postgres://{}@{}/{}".format(
            DATABASE_USER, DATABASE_LOCATION, DATABASE_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    from . import views, error_handlers
    app.register_blueprint(views.bp)
    app.register_blueprint(error_handlers.bp)

    return app

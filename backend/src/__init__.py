from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    database_name = 'flat-tutorials'
    database_path = "postgres://{}@{}/{}".format('postgres',
            'localhost:5432', database_name)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'vgT0?(XKnWvJfmnRW/:e'
    
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)
    
    from . import views, error_handlers
    app.register_blueprint(views.bp)
    app.register_blueprint(error_handlers.bp) 
    
    return app

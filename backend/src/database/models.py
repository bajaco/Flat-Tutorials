from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

database_name = 'database.db'
database_directory = Path(__file__).absolute()
database_path = "sqlite:///{}".format(database_directory / database_name)

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = 'flat-tutorials'
database_path = "postgres://{}@{}/{}".format('postgres','localhost:5432', database_name)

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.app = app
db.init_app(app)

migrate = Migrate(app,db)

#db.drop_all()
#db.creat_all()

import src.views

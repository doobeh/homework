from flask import Flask
from .database import db
from flask_bootstrap import Bootstrap
import os


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    default_sqlite_uri = os.path.join(app.instance_path, 'project.sqlite3')
    app.config.from_mapping(
        SECRET_KEY="default",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{default_sqlite_uri}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    app.config.from_pyfile("settings.cfg", silent=True)
    if config:
        app.config.from_pyfile(config)

    register_database(app)
    Bootstrap(app)

    return app


def register_database(app):
    db.init_app(app)
    return None

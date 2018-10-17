from werkzeug.utils import find_modules, import_string
from flask import Flask
from .database import db
from flask_bootstrap import Bootstrap
import os
from homework.cli import core_cli


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    default_sqlite_uri = os.path.join(app.instance_path, "project.sqlite3")
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
    register_blueprints(app)
    app.cli.add_command(core_cli)
    return app


def register_database(app):
    db.init_app(app)
    return None


def register_blueprints(app):
    """Register all blueprint modules
    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules("homework.blueprints"):
        mod = import_string(name)
        if hasattr(mod, "bp"):
            app.register_blueprint(mod.bp)
    return None

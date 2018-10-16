import os
from homework.models import User, Image, Metadata
from flask import current_app
from homework.database import db
from flask.cli import AppGroup
import click

core_cli = AppGroup("core")

@core_cli.command("init")
def app_init():
    if not os.path.exists(current_app.instance_path):
        os.makedirs(current_app.instance_path)
        print("[x] Created instance folder")
    db.create_all()
    print("[x] Created database")
    print("App is ready to launch. Run `flask run` to start a production server.")


@core_cli.command("nuke")
def app_init():
    db.drop_all()
    print("[x] Destroyed database")
    db.create_all()
    print("[x] Created database")
    if not os.path.exists(current_app.instance_path):
        os.makedirs(current_app.instance_path)
        print("[x] Created instance folder")
    print("App is ready to launch. Run `flask run` to start a production server.")


@core_cli.command("create")
@click.argument("email")
@click.password_option()
def user_create(email, password):
    # Lets check if the user exists already:
    u = User.query.filter_by(email=email).first()
    if u:
        return print("User Already Exists")
    u = User(email, password)
    db.session.add(u)
    db.session.commit()

    return print(f"User {u} created")

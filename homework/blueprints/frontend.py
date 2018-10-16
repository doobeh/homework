from flask import Blueprint, g, current_app, render_template
import os
from random import randint
from flask import jsonify, request, send_from_directory
from homework.database import db
from homework.models import User, Image, Metadata
from homework.auth import auth
from werkzeug.utils import secure_filename

bp = Blueprint("frontend", __name__, template_folder="templates", url_prefix="")


@bp.route('/')
def home():
    images = Image.query.all()
    return render_template('home.html', images=images)


@bp.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(current_app.instance_path, filename)
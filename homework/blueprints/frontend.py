from flask import Blueprint, current_app, render_template
from flask import send_from_directory
from homework.models import Image


bp = Blueprint("frontend", __name__, template_folder="templates", url_prefix="")


@bp.route("/")
def home():
    images = Image.query.all()
    return render_template("home.html", images=images)


@bp.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(current_app.instance_path, filename)

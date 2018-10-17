from flask import Blueprint, g, current_app
import os
from flask import jsonify, request
from homework.database import db
from homework.models import Image, Metadata
from homework.auth import auth
from werkzeug.utils import secure_filename
import uuid

bp = Blueprint("api", __name__, template_folder="templates", url_prefix="/api/v1")


@bp.route("/auth")
@auth.login_required
def create_token():
    if g.auth_type == "user":
        return jsonify(
            {
                "status": "success",
                "token": g.user.generate_token(),
                "message": "Login Successful",
            }
        )
    return (
        jsonify(
            {
                "status": "auth-failure",
                "message": "Token must be requested via user/pass combination",
            }
        ),
        401,
    )


@bp.route("/image", methods=["post"])
@auth.login_required
def image_upload():
    failed_message = {"status": "upload_failed", "message": "Upload failed"}

    if "image" not in request.files or g.auth_type == "user":
        return jsonify(failed_message), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify(failed_message), 400

    _, file_extension = os.path.splitext(secure_filename(file.filename))
    filename = f"{uuid.uuid4().hex}{file_extension}"
    file.save(os.path.join(current_app.instance_path, filename))
    i = Image(filename, g.user)
    db.session.add(i)
    db.session.commit()
    return jsonify(
        {"status": "success", "reference": i.id, "message": "File Uploaded."}
    )


@bp.route("/metadata", methods=["post"])
@auth.login_required
def metadata():
    data = request.json
    image = Image.query.filter_by(id=data["reference"]).first()
    if not image:
        return (
            jsonify(
                {"status": "bad_reference", "message": "Image reference lookup failure"}
            ),
            400,
        )
    try:
        md = Metadata(
            g.user, data["reference"], data["date"], data["description"], data["url"]
        )
        db.session.add(md)
        db.session.commit()
        return jsonify({"status": "success", "message": "Metadata Uploaded"})
    except KeyError:
        return (
            jsonify(
                {
                    "status": "meta_failure",
                    "message": "Meta-data failed-- missing data field",
                }
            ),
            400,
        )

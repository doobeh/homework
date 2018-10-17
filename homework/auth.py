from flask_httpauth import HTTPBasicAuth
from homework.models import User
from flask import g

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    auth_type = "token"
    user = User.verify_token(email_or_token)

    if not user:
        user = User.query.filter_by(email=email_or_token).first()
        auth_type = "user"
        if not user or not user.validate_password(password):
            return False
    g.user = user
    g.auth_type = auth_type
    return True

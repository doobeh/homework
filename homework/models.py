from homework.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, BadTimeSignature, SignatureExpired
from flask import current_app as app, jsonify
from dateutil import parser


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def generate_token(self):
        data = {
            'email': self.email,
            'id': self.id,
        }
        signer = URLSafeTimedSerializer(app.secret_key)
        return signer.dumps(data)

    @staticmethod
    def verify_token(token):
        decoder = URLSafeTimedSerializer(app.secret_key)
        try:
            data = decoder.loads(token, max_age=10*60)
        except SignatureExpired:
            print("Expired")
            return None  # valid token, but expired
        except (BadSignature, BadTimeSignature):
            return None
        user = User.query.get(data['id'])
        return user


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('images', lazy="dynamic"))
    path = db.Column(db.String, nullable=False)

    def __init__(self, path, user):
        self.path = path
        self.user = user


class Metadata(db.Model):
    __tablename__ = 'metadata'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    image = db.relationship('Image', backref=db.backref("metadata", uselist=False))
    dt = db.Column(db.DateTime)
    url = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('metadata', lazy="dynamic"))

    def __init__(self, user, reference, date, description, url):
        self.reference = reference
        self.dt = parser.parse(date)
        self.description = description
        self.url = url
        self.user = user

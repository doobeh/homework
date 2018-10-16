from itsdangerous import URLSafeTimedSerializer, BadSignature, BadTimeSignature


def validate_token(token):
    loader = URLSafeTimedSerializer(app.secret_key())
    try:
        loader.loads(token, max_age=10 * 60)  # 10 minutes.
        return loader["id"]
    except (BadSignature, BadTimeSignature):
        return False

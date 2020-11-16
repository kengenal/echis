from datetime import datetime, timedelta

import jwt

from echis.main import settings


def create_token(data):
    get_secret = settings.TOKEN_SECRET
    get_alg = settings.TOKEN_ALGORITHM
    exp = settings.EXP
    payload = data
    if not get_secret and not get_alg:
        raise Exception("Secret cannot be null")
    if not data:
        raise Exception("Data cannot be null")
    payload["exp"] = datetime.utcnow() + timedelta(minutes=exp)
    token = jwt.encode(payload, get_secret, algorithm=get_alg).decode("UTF-8")
    return token

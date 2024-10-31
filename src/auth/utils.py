from datetime import datetime, timedelta
import logging
import jwt
from uuid import uuid4
from passlib.context import CryptContext

from src.config import Config

password_context = CryptContext(schemes = ['bcrypt'])

#ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ACCESS_TOKEN_EXPIRE = 3600
REFRESH_TOKEN_EXPIRE = 3600

def generate_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh_token: bool = False) -> str:
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRE))
    payload['jti'] = str(uuid4())

    if refresh_token:
        payload['refresh_token'] = str(uuid4())

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET_KEY,
        algorithm = Config.JWT_ALGORITHM
    )

    return token

def decode_access_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms = [Config.JWT_ALGORITHM])
        return decoded_token
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

from graphql import GraphQLError
import jwt

from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
from argon2.exceptions import VerifyMismatchError

from app.db.database import Session
from app.db.models import User

from functools import wraps

ph = PasswordHasher()


SECRET_KEY = "job_board_app_secret!"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_TIME_MINUTES = 15


def generate_token(email):

    exp_time = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRATION_TIME_MINUTES
    )

    payload = {"sub": email, "exp": exp_time}

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def hash_password(pwd):
    return ph.hash(pwd)


def verify_password(pwd_hash, pwd):
    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")


def get_authenticated_user(context):
    request_object = context.get("request")
    auth_reader = request_object.headers.get("Authorization", "")

    if not auth_reader:
        raise GraphQLError("Invalid authentication token")

    token = auth_reader.split(" ")

    if len(token) != 2 or token[0] != "Bearer":
        raise GraphQLError("Invalid authentication token. The token must by provided by the following format: 'Bearer {token}'")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.exceptions.InvalidSignatureError:
        raise GraphQLError("Invalid authentication token")

    if datetime.now(timezone.utc) > datetime.fromtimestamp(
        payload["exp"], tz=timezone.utc
    ):
        raise GraphQLError("Token has expired")

    user = Session().query(User).filter(User.email == payload.get("sub")).first()

    if not user:
        raise GraphQLError("Could not authenticate user")

    return user


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)

        if user.role != "admin":
            raise GraphQLError("You are not authorized to perform this action")
        
        kwargs["logged_user"] = user
        
        return func(*args, **kwargs)

    return wrapper
    

def is_authenticated(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        
        get_authenticated_user(info.context)

        return func(*args, **kwargs)
    
    return wrapper
from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.dependencies import get_session
from fast_zero.models import User
from fast_zero.settings import Settings

pwrd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()


def get_password_hash(password: str):
    return pwrd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwrd_context.verify(plain_password, hashed_password)


def create_acess_token(data_payload: dict):
    to_encode = data_payload.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHN)

    return encode_jwt


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHN])
        subject_email: str = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user

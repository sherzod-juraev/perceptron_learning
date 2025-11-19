from datetime import datetime, timedelta
from typing import Annotated
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from .settings import setting


context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/')


# hash password
def hashed_pass(raw_password: str, /) -> str:
    return context.hash(raw_password)


def verify_pass(raw_password: str, hash_password: str, /) -> bool:
    return context.verify(raw_password, hash_password)


# token
def create_access(user_id: UUID, /) -> str:
    token_dict = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=setting.access_token_minutes)
    }
    token = jwt.encode(token_dict, setting.secret_key, setting.algorithm)
    return token


def create_refresh(user_id: UUID, /) -> str:
    token_dict = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=setting.refresh_token_days)
    }
    token = jwt.encode(token_dict, setting.secret_key, setting.algorithm)
    return token


def validate_access(token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user_id not found in access_token'
            )
        return UUID(user_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )


def validate_refresh(token: str, /) -> UUID:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Refresh token not found'
        )
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user_id not found in refresh_token'
            )
        return UUID(user_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired'
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token invalid'
        )
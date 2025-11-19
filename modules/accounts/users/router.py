from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from core import create_access, create_refresh, validate_access, validate_refresh, setting
from database import get_db
from . import User, UserIn, UserOut, UserUpdate, Token, crud


user_router = APIRouter()


@user_router.post(
    '/',
    summary='Create user',
    status_code=status.HTTP_201_CREATED,
    response_model=Token
)
async def create_user(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    user_scheme = UserIn(
        username=form_data.username,
        password=form_data.password
    )
    user_db = await crud.create(db, user_scheme)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh(user_db.id),
        expires=datetime.now(timezone.utc) + timedelta(days=setting.refresh_token_days),
        max_age=60 * 60 * 24 * setting.refresh_token_days,
        httponly=True
    )
    token = Token(
        access_token=create_access(user_db.id)
    )
    return token


@user_router.post(
    '/refresh',
    summary='access_token update by refresh_token',
    status_code=status.HTTP_200_OK,
    response_model=Token
)
async def token_update(
        request: Request,
        response: Response
) -> Token:
    token = request.cookies.get('refresh_token')
    user_id = validate_refresh(token)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh(user_id),
        expires=datetime.now(timezone.utc) + timedelta(days=setting.refresh_token_days),
        max_age=60 * 60 * 24 * setting.refresh_token_days,
        httponly=True
    )
    token = Token(
        access_token=create_access(user_id)
    )
    return token


@user_router.put(
    '/',
    summary='User full update',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def full_update(
        user_id: Annotated[UUID, Depends(validate_access)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.update(db, user_scheme, user_id)
    return user_db


@user_router.patch(
    '/',
    summary='User partial update',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def partial_update(
        user_id: Annotated[UUID, Depends(validate_access)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.update(db, user_scheme, user_id, True)
    return user_db


@user_router.delete(
    '/',
    summary='Delete user',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        user_id: Annotated[UUID, Depends(validate_access)],
        user_scheme: UserIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete(db, user_scheme, user_id)


@user_router.get(
    '/',
    summary='Get user',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def get_user(
        user_id: Annotated[UUID, Depends(validate_access)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.verify(db, user_id)
    return user_db
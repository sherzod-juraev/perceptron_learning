from datetime import datetime
from re import match
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class Token(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    access_token: str
    token_type: str = 'bearer'


class UserOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    username: str
    full_name: str | None = None
    created_at: datetime


class UserIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=25)


    @field_validator('username')
    def verify_username(cls, value):
        pattern = r'^[A-Za-z]{1}[A-Za-z\d_]{1,50}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username is wrong'
            )
        return value


    @field_validator('password')
    def verify_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{8,25}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password is wrong'
            )
        return value


class UserUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str | None = Field(None, max_length=50)
    password: str | None = Field(None, min_length=8, max_length=50)
    full_name: str | None = Field(None, max_length=100)

    @field_validator('username')
    def verify_username(cls, value):
        pattern = r'^[A-Za-z]{1}[A-Za-z\d_]{1,50}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username is wrong'
            )
        return value


    @field_validator('password')
    def verify_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{8,25}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password is wrong'
            )
        return value


    @field_validator('full_name')
    def verify_full_name(cls, value):
        pattern = r'^[A-Za-z ]{1,100}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Full name is wrong'
            )
        return value
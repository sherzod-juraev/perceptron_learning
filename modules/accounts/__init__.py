from fastapi import APIRouter


# import models
from .users import User

__all__ = ['User']

accounts_router = APIRouter()
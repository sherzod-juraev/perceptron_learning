from fastapi import APIRouter


# import models
from .users import User


__all__ = ['User']


# import routers
from .users.router import user_router


accounts_router = APIRouter()


accounts_router.include_router(
    user_router,
    prefix='/auth',
    tags=['Authenticate']
)
from fastapi import APIRouter


# import models
from .accounts import *


__all__ = ['User']


# import routers
from .accounts import accounts_router


modules_router = APIRouter()

modules_router.include_router(
    accounts_router
)
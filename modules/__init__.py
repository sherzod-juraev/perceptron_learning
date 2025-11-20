from fastapi import APIRouter, Depends
from core import validate_access


# import models
from .accounts import *


__all__ = ['User']


# import routers
from .accounts import accounts_router
from .perceptron.router import perceptron_router


modules_router = APIRouter()

modules_router.include_router(
    accounts_router
)

modules_router.include_router(
    perceptron_router,
    prefix='/perceptron',
    tags=['Perceptron model'],
    dependencies=[Depends(validate_access)]
)
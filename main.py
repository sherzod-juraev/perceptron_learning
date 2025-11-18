from fastapi import FastAPI
from core import register_exception
from modules import modules_router


app = FastAPI()

register_exception(app)

app.include_router(
    modules_router
)
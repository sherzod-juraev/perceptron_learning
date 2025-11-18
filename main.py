from fastapi import FastAPI
from core import register_exception


app = FastAPI()

register_exception(app)
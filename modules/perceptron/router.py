from typing import Annotated
from fastapi import APIRouter, status, Body
from numpy import array
from perceptron import Perceptron
from . import PerceptronIn, PerceptronOut

perceptron_model = Perceptron()

perceptron_router = APIRouter()


@perceptron_router.post(
    '/',
    summary='Learning perceptron',
    status_code=status.HTTP_200_OK,
    response_model=PerceptronOut
)
async def learning_perseptron(
    data_scheme: PerceptronIn
) -> list[float]:
    X = array(data_scheme.X)
    Y = array(data_scheme.Y)
    result = PerceptronOut(
        fit=perceptron_model.fit(X, Y),
        weights=list(perceptron_model.weights)
    )
    return result


@perceptron_router.post(
    '/predict',
    summary='Predict',
    status_code=status.HTTP_200_OK,
    response_model=int
)
async def predict(
        X: Annotated[list[float], Body()]
) -> int:
    X = array(X)
    result = perceptron_model.predict(X)
    return result
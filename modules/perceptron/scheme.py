from pydantic import BaseModel


class PerceptronOut(BaseModel):

    fit: str = True
    weights: list[float]


class PerceptronIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    X: list[list[float]]
    Y: list[int]
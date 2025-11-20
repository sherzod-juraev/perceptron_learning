from pydantic import BaseModel


class PerceptronIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    X: list[list[float]]
    Y: list[int]
from numpy import array
from numpy import unique, issubdtype, isnan, number
from fastapi import HTTPException, status


def preprocessing(X: array, Y: array, /):

    if X.ndim() != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='A 2D matrix must be inserted into X'
        )
    if isnan(X).any():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='NaN values found!'
        )
    if len(unique(Y)) != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Target must have exactly 2 classes!'
        )
    if not issubdtype(X.dtype, number):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='All features must be numeric!'
        )
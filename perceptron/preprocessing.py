from numpy import array, ndarray, integer
from numpy import unique, issubdtype, isnan, number
from fastapi import HTTPException, status


def preprocessing(X: ndarray, Y: ndarray, /):

    if X.ndim != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='A 2D matrix must be inserted into X'
        )
    if isnan(X).any():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='NaN values found!'
        )
    if not issubdtype(X.dtype, number):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='All features must be numeric!'
        )
    if len(unique(Y)) != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Target must have exactly 2 classes!'
        )
    if not issubdtype(Y.dtype, integer):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='classes must be integer'
        )
    if X.shape[0] != Y.shape[0]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='The lengths X and Y are not compatible.'
        )
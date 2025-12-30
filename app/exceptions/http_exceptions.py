from fastapi import HTTPException


def not_found(message: str = "Not found") -> HTTPException:
    return HTTPException(status_code=404, detail=message)


def unprocessable(message: str = "Validation error") -> HTTPException:
    return HTTPException(status_code=422, detail=message)
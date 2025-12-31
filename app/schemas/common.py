from typing import Any, Optional
from pydantic import BaseModel


class ErrorModel(BaseModel):
    code: int
    message: str


class FailureResponse(BaseModel):
    status: str = "failure"
    error: ErrorModel


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Any
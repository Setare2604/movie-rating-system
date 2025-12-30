from pydantic import BaseModel, Field
from datetime import datetime


class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=10)


class RatingOut(BaseModel):
    id: int
    movie_id: int
    score: int
    created_at: datetime
from pydantic import BaseModel, Field
from datetime import datetime


class RatingCreate(BaseModel):
    score: int 


class RatingOut(BaseModel):
    id: int
    movie_id: int
    score: int
    created_at: datetime
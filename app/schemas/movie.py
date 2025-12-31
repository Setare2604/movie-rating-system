from pydantic import BaseModel, Field
from typing import List, Optional


class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    release_year: Optional[int] = Field(None, ge=1800, le=3000)
    cast: Optional[str] = None
    director_id: int = Field(..., ge=1)
    genre_ids: List[int] = Field(default_factory=list)


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    release_year: Optional[int] = Field(None, ge=1800, le=3000)
    cast: Optional[str] = None
    director_id: Optional[int] = Field(None, ge=1)
    genre_ids: Optional[List[int]] = None
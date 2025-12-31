from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.common import SuccessResponse
from app.schemas.rating import RatingCreate
from app.services.rating_service import RatingService

router = APIRouter(prefix="/api/v1/movies", tags=["ratings"])


@router.post("/{movie_id}/ratings", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_rating(movie_id: int, payload: RatingCreate, db: Session = Depends(get_db)):
    service = RatingService(db)
    data = service.create_rating(movie_id=movie_id, score=payload.score)
    return {"status": "success", "data": data}


@router.get("/{movie_id}/ratings", response_model=SuccessResponse)
def list_ratings(movie_id: int, db: Session = Depends(get_db)):
    service = RatingService(db)
    data = service.list_ratings(movie_id=movie_id)
    return {"status": "success", "data": data}
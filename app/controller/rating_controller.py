from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.movie_repository import MovieRepository
from app.repositories.rating_repository import RatingRepository
from app.schemas.rating import RatingCreate
from app.exceptions.http_exceptions import not_found
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/api/v1/movies", tags=["ratings"])


@router.post("/{movie_id}/ratings", response_model=SuccessResponse)
def create_rating(movie_id: int, payload: RatingCreate, db: Session = Depends(get_db)):
    # اول مطمئن شو فیلم وجود دارد
    movie_repo = MovieRepository(db)
    if movie_repo.get_movie(movie_id) is None:
        raise not_found("Movie not found")

    repo = RatingRepository(db)
    rating = repo.create_rating(movie_id=movie_id, score=payload.score)

    return {
        "status": "success",
        "data": {
            "id": rating.id,
            "movie_id": rating.movie_id,
            "score": rating.score,
            "created_at": rating.created_at,
        },
    }


@router.get("/{movie_id}/ratings", response_model=SuccessResponse)
def list_ratings(movie_id: int, db: Session = Depends(get_db)):
    movie_repo = MovieRepository(db)
    if movie_repo.get_movie(movie_id) is None:
        raise not_found("Movie not found")

    repo = RatingRepository(db)
    ratings = repo.list_ratings(movie_id)

    return {
        "status": "success",
        "data": [
            {
                "id": r.id,
                "movie_id": r.movie_id,
                "score": r.score,
                "created_at": r.created_at,
            }
            for r in ratings
        ],
    }
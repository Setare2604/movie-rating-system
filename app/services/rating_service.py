from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.movie_repository import MovieRepository
from app.repositories.rating_repository import RatingRepository
from app.exceptions.http_exceptions import not_found, unprocessable


def _to_iso_z(dt):
    if dt is None:
        return None
    s = dt.isoformat()
    return s.replace("+00:00", "Z")


class RatingService:
    def __init__(self, db: Session):
        self.db = db
        self.movie_repo = MovieRepository(db)
        self.rating_repo = RatingRepository(db)

    def create_rating(self, movie_id: int, score: int) -> dict:
        if self.movie_repo.get_movie(movie_id) is None:
            raise not_found("Movie not found")

        if score < 1 or score > 10:
            raise unprocessable("Score must be an integer between 1 and 10")

        rating = self.rating_repo.create_rating(movie_id=movie_id, score=score)
        return {
            "rating_id": rating.id,
            "movie_id": rating.movie_id,
            "score": rating.score,
            "created_at": _to_iso_z(rating.created_at),
        }

    def list_ratings(self, movie_id: int) -> list[dict]:
        if self.movie_repo.get_movie(movie_id) is None:
            raise not_found("Movie not found")

        ratings = self.rating_repo.list_ratings(movie_id)
        return [
            {
                "id": r.id,
                "movie_id": r.movie_id,
                "score": r.score,
                "created_at": _to_iso_z(r.created_at),
            }
            for r in ratings
        ]
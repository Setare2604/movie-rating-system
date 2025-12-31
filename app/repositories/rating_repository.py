from sqlalchemy.orm import Session
from app.models.movie_rating import MovieRating


class RatingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_rating(self, movie_id: int, score: int) -> MovieRating:
        rating = MovieRating(movie_id=movie_id, score=score)
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def list_ratings(self, movie_id: int):
        return (
            self.db.query(MovieRating)
            .filter(MovieRating.movie_id == movie_id)
            .order_by(MovieRating.created_at.desc())
            .all()
        )
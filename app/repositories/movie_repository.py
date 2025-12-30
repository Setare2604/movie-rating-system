from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_rating import MovieRating
from app.models.director import Director


class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_movies(self, page: int, page_size: int, title: str | None, release_year: int | None, genre: str | None):
        q = (
            self.db.query(
                Movie,
                func.count(MovieRating.id).label("ratings_count"),
                func.avg(MovieRating.score).label("average_rating"),
            )
            .outerjoin(MovieRating, MovieRating.movie_id == Movie.id)
            .join(Director, Director.id == Movie.director_id)
            .group_by(Movie.id)
        )

        # filters (AND)
        if title:
            q = q.filter(Movie.title.ilike(f"%{title}%"))
        if release_year is not None:
            q = q.filter(Movie.release_year == release_year)
        if genre:
            q = q.join(Movie.genres).filter(Genre.name.ilike(f"%{genre}%"))

        total = q.count()

        rows = (
            q.order_by(Movie.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = []
        for movie, ratings_count, average_rating in rows:
            items.append(
                {
                    "id": movie.id,
                    "title": movie.title,
                    "release_year": movie.release_year,
                    "cast": movie.cast,
                    "director": {"id": movie.director.id, "name": movie.director.name},
                    "genres": [{"id": g.id, "name": g.name} for g in movie.genres],
                    "ratings_count": int(ratings_count or 0),
                    "average_rating": round(float(average_rating), 2) if average_rating is not None else None,
                }
            )

        return items, total
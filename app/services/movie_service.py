from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, MovieUpdate
from app.exceptions.http_exceptions import not_found, unprocessable


class MovieService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MovieRepository(db)

    def list_movies(
        self,
        *,
        page: int,
        page_size: int,
        title: str | None,
        release_year: int | None,
        genre: str | None,
    ) -> dict:
        items, total = self.repo.list_movies(
            page=page,
            page_size=page_size,
            title=title,
            release_year=release_year,
            genre=genre,
        )
        return {
            "page": page,
            "page_size": page_size,
            "total_items": total,
            "items": items,
        }

    def create_movie(self, payload: MovieCreate) -> dict:
        movie, err = self.repo.create_movie(payload)
        if err:
            raise unprocessable(err)
        return movie

    def get_movie(self, movie_id: int) -> dict:
        movie = self.repo.get_movie(movie_id)
        if movie is None:
            raise not_found("Movie not found")
        return movie

    def update_movie(self, movie_id: int, payload: MovieUpdate) -> dict:
        movie, err = self.repo.update_movie(movie_id, payload)
        if err:
            if err == "Movie not found":
                raise not_found(err)
            raise unprocessable(err)
        return movie

    def delete_movie(self, movie_id: int) -> None:
        ok = self.repo.delete_movie(movie_id)
        if not ok:
            raise not_found("Movie not found")
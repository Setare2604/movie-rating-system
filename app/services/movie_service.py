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
        director = self.repo.get_director_by_id(payload.director_id)
        if director is None:
            raise unprocessable("Invalid director_id or genres")

        genre_ids = getattr(payload, "genre_ids", None) or getattr(payload, "genres", [])
        genres = self.repo.get_genres_by_ids(genre_ids)
        if len(genres) != len(set(genre_ids)):
            raise unprocessable("Invalid director_id or genres")

        return self.repo.create_movie(payload, genres)        

    def get_movie(self, movie_id: int) -> dict:
        movie = self.repo.get_movie(movie_id)
        if movie is None:
            raise not_found("Movie not found")
        return movie

    def update_movie(self, movie_id: int, payload: MovieUpdate) -> dict:
        if self.repo.get_movie(movie_id) is None:
            raise not_found("Movie not found")

        if payload.director_id is not None:
            director = self.repo.get_director_by_id(payload.director_id)
            if director is None:
                raise unprocessable("Invalid director_id or genres")

        genres = None
        if hasattr(payload, "genre_ids") and payload.genre_ids is not None:
            gids = payload.genre_ids
            genres = self.repo.get_genres_by_ids(gids) if gids else []
            if len(genres) != len(set(gids)):
                raise unprocessable("Invalid director_id or genres")
        updated = self.repo.update_movie(movie_id, payload, genres)
        return updated

    def delete_movie(self, movie_id: int) -> None:
        ok = self.repo.delete_movie(movie_id)
        if not ok:
            raise not_found("Movie not found")
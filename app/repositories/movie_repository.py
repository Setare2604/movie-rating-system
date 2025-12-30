from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_rating import MovieRating
from app.models.director import Director
from app.schemas.movie import MovieCreate, MovieUpdate
from sqlalchemy.orm import joinedload


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
    
    def get_movie(self, movie_id: int):
        row = (
            self.db.query(
                Movie,
                func.count(MovieRating.id).label("ratings_count"),
                func.avg(MovieRating.score).label("average_rating"),
            )
            .outerjoin(MovieRating, MovieRating.movie_id == Movie.id)
            .filter(Movie.id == movie_id)
            .group_by(Movie.id)
            .options(joinedload(Movie.director), joinedload(Movie.genres))
            .first()
        )

        if not row:
            return None

        movie, ratings_count, average_rating = row

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "cast": movie.cast,
            "director": {"id": movie.director.id, "name": movie.director.name},
            "genres": [{"id": g.id, "name": g.name} for g in movie.genres],
            "ratings_count": int(ratings_count or 0),
            "average_rating": round(float(average_rating), 2) if average_rating is not None else None,
        }
    
    def create_movie(self, payload: MovieCreate):
        # validate director exists
        director = self.db.query(Director).filter(Director.id == payload.director_id).first()
        if director is None:
            return None, "Invalid director_id"

        # validate genres
        genres = []
        if payload.genre_ids:
            genres = self.db.query(Genre).filter(Genre.id.in_(payload.genre_ids)).all()
            if len(genres) != len(set(payload.genre_ids)):
                return None, "Invalid genre_ids"

        movie = Movie(
            title=payload.title,
            release_year=payload.release_year,
            cast=payload.cast,
            director_id=payload.director_id,
        )

        movie.genres = genres  # works because of secondary=genres_movie :contentReference[oaicite:2]{index=2}

        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)

        # reuse get_movie output format
        return self.get_movie(movie.id), None

    def update_movie(self, movie_id: int, payload: MovieUpdate):
        movie_obj = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if movie_obj is None:
            return None, "Movie not found"

        if payload.director_id is not None:
            director = self.db.query(Director).filter(Director.id == payload.director_id).first()
            if director is None:
                return None, "Invalid director_id"
            movie_obj.director_id = payload.director_id

        if payload.title is not None:
            movie_obj.title = payload.title
        if payload.release_year is not None:
            movie_obj.release_year = payload.release_year
        if payload.cast is not None:
            movie_obj.cast = payload.cast

        if payload.genre_ids is not None:
            if payload.genre_ids:
                genres = self.db.query(Genre).filter(Genre.id.in_(payload.genre_ids)).all()
                if len(genres) != len(set(payload.genre_ids)):
                    return None, "Invalid genre_ids"
                movie_obj.genres = genres
            else:
                movie_obj.genres = []

        self.db.commit()
        self.db.refresh(movie_obj)
        return self.get_movie(movie_id), None

    def delete_movie(self, movie_id: int):
        movie_obj = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if movie_obj is None:
            return False
        self.db.delete(movie_obj)
        self.db.commit()
        return True
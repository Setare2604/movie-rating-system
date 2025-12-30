from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.movie_repository import MovieRepository
from app.schemas.common import SuccessResponse
from app.exceptions.http_exceptions import unprocessable
from app.exceptions.http_exceptions import not_found
from app.schemas.movie import MovieCreate, MovieUpdate

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.get("", response_model=SuccessResponse)
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    title: str | None = None,
    release_year: str | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    year: int | None = None
    if release_year is not None:
        if not release_year.isdigit():
            raise unprocessable("Invalid release_year")
        year = int(release_year)

    repo = MovieRepository(db)
    items, total = repo.list_movies(
        page=page,
        page_size=page_size,
        title=title,
        release_year=year,
        genre=genre,
    )
    return {
        "status": "success",
        "data": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "items": items,
        },
    }

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    repo = MovieRepository(db)
    movie, err = repo.create_movie(payload)

    if err:
        raise unprocessable(err)

    return {"status": "success", "data": movie}

@router.get("/{movie_id}", response_model=SuccessResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    repo = MovieRepository(db)
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise not_found("Movie not found")

    return {"status": "success", "data": movie}

@router.put("/{movie_id}", response_model=SuccessResponse)
def update_movie(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    repo = MovieRepository(db)
    movie, err = repo.update_movie(movie_id, payload)

    if err:
        if err == "Movie not found":
            raise not_found(err)
        raise unprocessable(err)

    return {"status": "success", "data": movie}

@router.delete("/{movie_id}", response_model=SuccessResponse)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    repo = MovieRepository(db)
    ok = repo.delete_movie(movie_id)
    if not ok:
        raise not_found("Movie not found")
    return {"status": "success", "data": {"message": "Movie deleted"}}
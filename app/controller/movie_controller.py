from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.common import SuccessResponse
from app.schemas.movie import MovieCreate, MovieUpdate
from app.exceptions.http_exceptions import unprocessable
from app.services.movie_service import MovieService

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

    service = MovieService(db)
    data = service.list_movies(
        page=page,
        page_size=page_size,
        title=title,
        release_year=year,
        genre=genre,
    )
    return {"status": "success", "data": data}


@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    service = MovieService(db)
    movie = service.create_movie(payload)
    return {"status": "success", "data": movie}


@router.get("/{movie_id}", response_model=SuccessResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    movie = service.get_movie(movie_id)
    return {"status": "success", "data": movie}


@router.put("/{movie_id}", response_model=SuccessResponse)
def update_movie(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    service = MovieService(db)
    movie = service.update_movie(movie_id, payload)
    return {"status": "success", "data": movie}


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    service.delete_movie(movie_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
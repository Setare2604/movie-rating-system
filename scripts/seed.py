from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.movie_rating import MovieRating


def get_or_create(session: Session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    params = dict(kwargs)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    session.add(instance)
    session.flush()
    return instance


def main():
    db = SessionLocal()
    try:
        # Directors
        nolan = get_or_create(db, Director, name="Christopher Nolan", defaults={"birth_year": 1970})
        fincher = get_or_create(db, Director, name="David Fincher", defaults={"birth_year": 1962})

        # Genres
        drama = get_or_create(db, Genre, name="Drama")
        sci_fi = get_or_create(db, Genre, name="Sci-Fi")
        thriller = get_or_create(db, Genre, name="Thriller")

        # Movies
        inception = get_or_create(
            db,
            Movie,
            title="Inception",
            director_id=nolan.id,
            defaults={"release_year": 2010, "cast": "Leonardo DiCaprio"}
        )
        fight_club = get_or_create(
            db,
            Movie,
            title="Fight Club",
            director_id=fincher.id,
            defaults={"release_year": 1999, "cast": "Brad Pitt, Edward Norton"}
        )

        # Genres assignment (many-to-many)
        if sci_fi not in inception.genres:
            inception.genres.append(sci_fi)
        if thriller not in inception.genres:
            inception.genres.append(thriller)
        if drama not in fight_club.genres:
            fight_club.genres.append(drama)
        if thriller not in fight_club.genres:
            fight_club.genres.append(thriller)

        db.flush()

        # Ratings (فقط اگر برای آن فیلم rating نداریم، اضافه کن)
        def add_rating_if_missing(movie: Movie, score: int):
            exists = db.query(MovieRating).filter(MovieRating.movie_id == movie.id, MovieRating.score == score).first()
            if not exists:
                db.add(MovieRating(movie_id=movie.id, score=score))

        add_rating_if_missing(inception, 9)
        add_rating_if_missing(inception, 8)
        add_rating_if_missing(fight_club, 10)

        db.commit()
        print("Seed completed successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
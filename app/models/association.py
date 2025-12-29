from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from app.db.database import Base

genres_movie = Table(
    "genres_movie",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("movie_id", "genre_id", name="uq_genres_movie_movie_genre"),
)
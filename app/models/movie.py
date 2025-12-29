from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.association import genres_movie

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    release_year = Column(Integer, nullable=True)
    cast = Column(Text, nullable=True)

    director_id = Column(Integer, ForeignKey("directors.id", ondelete="RESTRICT"), nullable=False)

    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=genres_movie, back_populates="movies")
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete-orphan")
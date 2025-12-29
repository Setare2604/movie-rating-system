from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class MovieRating(Base):
    __tablename__ = "movie_ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)

    score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("score >= 1 AND score <= 10", name="ck_movie_ratings_score_range"),
    )

    movie = relationship("Movie", back_populates="ratings")
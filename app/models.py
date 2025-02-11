from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


# Book model maps to the "books" table in PostgreSQL
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String, index=True)
    avg_rating = Column(Float)
    review_count = Column(Integer)
    description = Column(Text)
    url = Column(String)

from sqlalchemy import Column, Integer, String, Float, Text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# Book model maps to the "books" table in PostgreSQL
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String)
    avg_rating = Column(Float)
    review_count = Column(Integer)
    description = Column(Text)
    url = Column(String)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)

    list = relationship("BookList")

    # __table_args__ = (UniqueConstraint("title", "author", name="unique_book"),)


class BookList(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
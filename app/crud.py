from sqlalchemy.orm import Session
from sqlalchemy import select, update, bindparam, delete
import models, schemas


# CREATE: Add a new list
def create_list(db: Session, list_name: str):
    new_list = models.BookList(name=list_name)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

def get_all_lists(db: Session):
    stmt = select(models.BookList)
    result = db.execute(stmt).scalars().all()
    updated_result = []
    for book_list in result:
        book_count = db.query(models.Book).filter(models.Book.list_id == book_list.id).count()
        updated_result.append({"id": book_list.id, "name": book_list.name, "book_count": book_count})
    return updated_result

def get_list(db: Session, list_id: int):
    stmt = select(models.BookList).where(models.BookList.id == list_id)
    result = db.execute(stmt).scalars().all()
    return result

def create_book(db: Session, book: schemas.BookCreate, list_id=1):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        review_count=book.review_count,
        avg_rating=book.avg_rating,
        list_id=list_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    print(f"Book added: {db_book.title} by {db_book.author}")
    return db_book

def get_all_books(db:Session):
    stmt = select(models.Book)
    result = db.execute(stmt).scalars().all()
    return result

def get_books_by_list(db: Session, list_id: int):
    stmt = select(models.Book).where(models.Book.list_id == list_id)
    result = db.execute(stmt).scalars().all()
    return result

def update_list_name(db: Session, list_id: int, new_name: str):
    stmt = (update(models.BookList)
            .where(models.BookList.id == list_id)
            .values(name = new_name))
    result = db.execute(stmt).rowcount
    db.commit()
    return result

def delete_list(db: Session, list_id: int):
    stmt = delete(models.BookList).where(models.BookList.id == list_id)
    result = db.execute(stmt).rowcount
    db.commit()
    return result
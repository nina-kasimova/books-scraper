from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
import schemas
from database import SessionLocal, engine
import models
from scraper import scrape_books
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import crud
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOGETHERAI_TOKEN = os.environ.get("TOGETHERAI_TOKEN")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],   # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],   # Allow all headers
)


models.Base.metadata.create_all(bind=engine)

scraped_books = []
scraping_status = {"status": "idle"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {TOGETHERAI_TOKEN}"}

@app.post("/get_recommendations")
def get_recommendations(prompt: str):
    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, json=data, headers=HEADERS)

    return response.json()

@app.post("/test_google")
def get_book_info(book_title):
    url = f'https://www.googleapis.com/books/v1/volumes?q={book_title}'
    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        book = data['items'][0]['volumeInfo']
        title = book.get('title', 'No title')
        author = ', '.join(book.get('authors', ['Unknown author']))
        genre = ', '.join(book.get('categories', ['No genre']))
        description = book.get('description', 'No description available.')

        return {
            'title': title,
            'author': author,
            'genre': genre,
            'description': description
        }
    else:
        return None


book_info = get_book_info('The Catcher in the Rye')
print(book_info)


@app.post("/add_list")
def create_list(list_data: schemas.ListCreate, db: Session = Depends(get_db)):
    db_list = crud.create_list(db, list_data.name)
    return db_list

@app.get("/lists")
def get_lists(db: Session = Depends(get_db)):
    return crud.get_all_lists(db)

@app.get("/list_by_id")
def get_list_byId(list_id: int, db: Session = Depends(get_db)):
    return crud.get_list(db, list_id)


@app.post("/add_book")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(db, book)

    return db_book


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def get_status():
    return {"scraping_status": scraping_status["status"]}


@app.post("/scrape")
async def start_scraping(url: str, list_id: int, background_tasks: BackgroundTasks):
    if scraping_status['status'] == "in progress":
        return {"message": "Scraping is already in progress. Please wait until it's completed."}

    scraping_status['status'] = "in progress"
    background_tasks.add_task(run_scraper, url, list_id)
    return {"message": "Scraping started!", "url": url, "list ID": list_id}


@app.get("/books")
async def get_books():
    if not scraped_books:
        return {"message": "No books scraped yet. Please run /scrape first."}
    return scraped_books

@app.get("/get_books_byList")
async def get_books_byList(list_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_list(db, list_id)

@app.get("/all_books")
async def get_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)

@app.post("/edit_list_name")
async def edit_list_name(list_id: int, new_name:str, db: Session = Depends(get_db)):
    return crud.update_list_name(db, list_id, new_name)

@app.post("/delete_list")
async def delete_list(list_id: int, db: Session = Depends(get_db)):
    return crud.delete_list(db, list_id)

async def run_scraper(url, list_id=1):
    global scraped_books
    print("🚀 Scraping started...")

    try:
        async for book in scrape_books(url):
            db = SessionLocal()
            try:

                # Check if book already exists before inserting
                existing_book = db.execute(select(models.Book).where(
                    models.Book.title == book["title"],
                    models.Book.list_id == list_id
                )).fetchone()

                if existing_book:
                    print(f"⚠️ Skipping duplicate: {book['title']} by {book['author']}")
                    continue

                scraped_books.append(book)

                print(f"✅ Inserting: {book['title']} by {book['author']}")
                # Insert new book if it's not a duplicate
                db_book = models.Book(
                    title=book["title"],
                    author=book["author"],
                    genre=book.get('genre', None),
                    review_count=book["review_count"],
                    avg_rating=book["avg_rating"],
                    url=book["book_link"],
                    cover_url=book["cover_url"],
                    list_id=list_id
                )
                db.add(db_book)

                db.commit()
            except Exception as e:
                print(f"❌ Error processing {book['title']}: {e}")
                db.rollback()
            finally:
                db.close()

        scraping_status["status"] = "completed"
        print("✅ Scraping completed successfully!")

    except Exception as e:
        scraping_status["status"] = "error"
        print(f"❌ Scraping failed with error: {e}")




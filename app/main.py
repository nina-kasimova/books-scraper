from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from scraper import scrape_books
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


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


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    review_count: int
    avg_rating: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_book")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(title=book.title, author=book.author, genre=book.genre, review_count=book.review_count, avg_rating=book.avg_rating)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    print(f"Book added: {db_book.title} by {db_book.author}")

    return db_book


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def get_status():
    return {"scraping_status": scraping_status["status"]}


@app.get("/scrape")
async def start_scraping(background_tasks: BackgroundTasks):
    scraping_status['status'] = "in progress"
    background_tasks.add_task(run_scraper)
    return {"message": "Scraping started!"}


@app.get("/books")
async def get_books():
    if not scraped_books:
        return {"message": "No books scraped yet. Please run /scrape first."}
    return scraped_books


async def run_scraper():
    global scraped_books
    print("🚀 Scraping started...")

    try:
        books_info = await scrape_books()
        scraped_books = books_info
        scraping_status["status"] = "completed"

        if not isinstance(books_info, list):
            raise ValueError("❌ Expected books_info to be a list, but got something else.")

        print("✅ Scraping completed successfully!")

        db = SessionLocal()

        for book in books_info:
            db_book = models.Book(
                title=book["title"],
                author=book["author"],
                review_count=book["review_count"],
                avg_rating=book["avg_rating"]
            )
            db.add(db_book)

        db.commit()
        db.close()

    except Exception as e:
        scraping_status["status"] = "error"
        print(f"❌ Scraping failed with error: {e}")




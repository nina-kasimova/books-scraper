import requests
import pandas as pd
import models
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import random

# Synchronous function to get book info from Google Books API
def get_google_info_test(book_title, max_retries=5, delay=2):
    url = f'https://www.googleapis.com/books/v1/volumes?q={book_title}'
    retries = 0

    time.sleep(3
    )

    while retries < max_retries:
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if 'items' in data:
                book = data['items'][0]['volumeInfo']
                title = book.get('title', 'No title')
                genre = ', '.join(book.get('categories', ['No genre']))
                description = book.get('description', 'No description available.')
                cover_url = book.get('imageLinks', {}).get('thumbnail', 'No cover image')
                return {
                    'genre': genre,
                    'description': description,
                    'cover_url': cover_url,
                    'title': title
                }
            else:
                print(f"MISSING INFO FOR BOOK {book_title}")
                retries += 1
                if retries < max_retries:
                    # Exponential backoff: delay increases after each failure
                    delay = min(30, delay * 2)  # Limit maximum delay to 30 seconds
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to fetch data for {book_title} after {max_retries} retries.")
                    return {
                        'genre': 'No genre',
                        'description': 'No description available.',
                        'cover_url': 'No cover image',
                        'title': book_title  # Keep original title in case of failure
                    }
        except requests.exceptions.RequestException as e:
            print(f"Request error for {book_title}: {e}, retrying...")
            retries += 1
            if retries < max_retries:
                jitter = random.uniform(0.5, 1.5)  # Small random jitter for delay
                delay = min(30, delay * 2 + jitter)  # Exponential backoff with jitter
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to fetch data for {book_title} after {max_retries} retries.")
                return {
                    'genre': 'No genre',
                    'description': 'No description available.',
                    'cover_url': 'No cover image',
                    'title': book_title
                }

    return None

# Update function that processes all books and makes synchronous API calls
def update_info(df):
    for index, row in df.iterrows():
        book_title = row['title']
        book_info = get_google_info_test(book_title)

        if book_info:
            print(f"Index {index} - Book: {book_info['title']}")
            df.loc[index, 'cover_url'] = book_info['cover_url']
            df.loc[index, 'description'] = book_info['description']
            df.loc[index, 'genre'] = book_info['genre']

    df.to_csv("updated_books_info.csv", index=False)
    print("Updated CSV file with book information.")

def insert_data(df):
    load_dotenv()
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL is not set. Check your .env file.")

    engine = create_engine(DATABASE_URL)
    # Connect to the database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    #-------- PREPARE DATA ---------
    books_to_insert = []

    for _, row in df.iterrows():
        read_status_value = row["read_status"] if row["read_status"] else "None"
        # Ensure that read_status is a valid ReadStatusEnum
        if read_status_value == "read":
            read_status_value = "Read"
        elif read_status_value == "to-read":
            read_status_value = "To-read"
        else:
            read_status_value = "None"  # Default value for None

        book = models.Book(
            title=row["title"],
            author=row["author"],
            genre=row["genre"],
            description=row["description"],
            review_count=row["review_count"],
            avg_rating=row["avg_rating"],
            my_rating=row["my_rating"],
            url=row["url"],
            cover_url=row["cover_url"],
            list_id=row["list_id"],
            read_status=read_status_value,  # Set read_status as Enum
            private_notes=row["private_notes"]
        )
        books_to_insert.append(book)

    # Add all books to the session and commit the transaction
    session.add_all(books_to_insert)
    session.commit()

    # Close the session
    session.close()

    print(f"Successfully inserted {len(books_to_insert)} books into the database.")

if __name__ == "__main__":
    df = pd.read_csv("/Users/nina/Desktop/py/books-scraper/app/updated_books_info.csv")

    insert_data(df)
    # df = df[:20]
    # Rename and select only necessary columns
    # df = df.rename(columns={
    #     "Title": "title",
    #     "Author": "author",
    #     "Average Rating": "avg_rating",
    #     "My Rating": "my_rating",
    #     "Private Notes": "private_notes",
    #     "Exclusive Shelf": "read_status"
    # })
    #
    # # Add missing columns
    # df["genre"] = "Unknown"  # Placeholder if genre isn't available
    # df["description"] = ""  # Empty string for now
    # df["review_count"] = 0  # No review count in CSV, setting default to 0
    # df["url"] = ""  # Placeholder URL
    # df["cover_url"] = ""  # Placeholder cover URL
    # df["list_id"] = 52
    #
    # # Define the columns you want to keep
    # required_columns = [
    #     "title", "author", "genre", "description", "review_count", "avg_rating",
    #     "my_rating", "url", "cover_url", "list_id", "read_status", "private_notes"
    # ]
    #
    # # Filter the DataFrame to only keep the necessary columns
    # df_filtered = df[required_columns]
    #
    # pd.set_option("display.max_columns", 12)
    # pd.set_option('display.max_colwidth', None)
    # selected_columns = ["title", "cover_url"]  # Replace with your desired columns
    # print(df_filtered[selected_columns].head(20))

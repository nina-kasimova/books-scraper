from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for ORM models to inherit from
Base = declarative_base()

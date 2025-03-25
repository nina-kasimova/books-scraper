from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    review_count: int
    avg_rating: float
    url: str
    cover_url: str
    list_id: int

class ListCreate(BaseModel):
    name: str  # The name of the book list

class ListResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
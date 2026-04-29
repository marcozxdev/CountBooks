from src.models.bookModel import BookModel
from src.repository.bookRepo import BookRepo
from src.database.database import Database




class BookService:
    def __init__(self, repo: BookRepo, db: Database, model: BookModel):
        self.repo = repo
        self.db = db


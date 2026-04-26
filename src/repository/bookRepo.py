from database.database import Database
from models.bookModel import BookModel

class BookRepo:
    def __init__(self, db: Database, book: BookModel):
        self.db = db
        self.book = book


    def get_books(self):
        pass

    def get_book(self):
        pass

    
    def add_book(self, book: BookModel):
        insert_book = book.a_book()

    
    def update_book(self):
        pass


    def delete_book(self):
        pass



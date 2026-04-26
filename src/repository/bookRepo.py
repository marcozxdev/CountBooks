from database.database import Database
# from models.bookModel import BookModel

class BookRepo:
    def __init__(self, db: Database):
        self.db = db


    def get_books(self):
        self.db.execute("")

    def get_book(self):
        pass

    
    def add_book(self, book: dict[str, any]):
        pass

    
    def add_books(self, books: list[dict]):
        pass


    def update_book(self):
        pass


    def delete_book(self):
        pass



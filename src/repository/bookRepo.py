from src.database.database import Database
from src.models.bookModel import BookModel
from src.repository.sqlite import Sqlite




class BookRepo:
    def __init__(self, db: Database):
        self.db = db

    def get_books(self, quantity: int):
        if quantity:
            self.db.execute("SELECT * FROM libros LIMIT ?", (quantity,))
            books = self.db.fetchall()
            return books
        return None
    

    def search_book(self, book, limit=10):
        if book:
            book = f"%{book}%"
            self.db.execute("""
            SELECT * FROM libros
            WHERE       titulo  like ? OR
                        categoria like ? OR
                        editorial  like ? OR
                        codigo_ref like ? OR
                        codigo_isbn like ? OR
                        referencia like ? OR
                        estado like ? OR
                        autor like ? 
            LIMIT ?;
            """,(book, book, book, book, book, book, book, book, limit))
            return self.db.fetchall()


    def get_book(self, book):
        return self.search_book(book, limit=1)

    
    def add_book(self, book: BookModel):
        self.db.execute("""
            INSERT INTO libros (titulo, categoria, editorial, codigo_ref, codigo_isbn, referencia, cantidad, estado, autor, prestado, donado, fecha) VALUES
            (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (book.titulo, book.categoria, book.editorial, book.codigo_ref, book.codigo_isbn, book.referencia, book.cantidad, book.estado, book.autor,  book.prestado, book.donado, book.fecha))

    
    def add_books(self, books):
        pass


    def update_book(self, book, new_book):
        pass


    def delete_book(self, book):
        pass




#### apartado de tests

# query = BookRepo(Sqlite())
# print(query.search_book("cien"))
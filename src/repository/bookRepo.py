from src.database.database import Database
from src.models.bookModel import BookModel


class BookRepo:
    def __init__(self, db: Database):
        self.db = db

    # -------------------------
    # Helpers internos
    # -------------------------

    def _fila_a_model(self, fila: tuple) -> BookModel:
        """Convierte una fila de la DB en un BookModel."""
        if fila is None:
            return None
        libro = BookModel(
            titulo      = fila[1],
            categoria   = fila[2],
            editorial   = fila[3],
            codigo_ref  = fila[4],
            codigo_isbn = fila[5],
            referencia  = fila[6],
            cantidad    = fila[7],
            estado      = fila[8],
            autor       = fila[9],
            prestado    = fila[10],
            donado      = fila[11],
            fecha       = fila[12],
        )
        libro.id = fila[0]
        return libro

    def _filas_a_models(self, filas: list) -> list:
        """Convierte una lista de filas en lista de BookModel."""
        return [self._fila_a_model(f) for f in filas]

    # -------------------------
    # Lectura
    # -------------------------

    def get_books(self, quantity: int = None) -> list:
        """Retorna todos los libros, o un límite si se especifica."""
        if quantity:
            self.db.execute("SELECT * FROM libros LIMIT ?", (quantity,))
        else:
            self.db.execute("SELECT * FROM libros")
        return self._filas_a_models(self.db.fetchall())

    def get_book_by_id(self, book_id: int) -> BookModel:
        """Retorna un libro por su ID."""
        self.db.execute("SELECT * FROM libros WHERE id = ?", (book_id,))
        return self._fila_a_model(self.db.fetchone())

    def search_books(self, query: str, limit: int = 10) -> list:
        """
        Busca libros por texto en los campos principales.
        Retorna una lista de BookModel.
        """
        if not query:
            return []
        q = f"%{query}%"
        self.db.execute("""
            SELECT * FROM libros
            WHERE   titulo      LIKE ? OR
                    categoria   LIKE ? OR
                    editorial   LIKE ? OR
                    codigo_ref  LIKE ? OR
                    codigo_isbn LIKE ? OR
                    referencia  LIKE ? OR
                    estado      LIKE ? OR
                    autor       LIKE ?
            LIMIT ?
        """, (q, q, q, q, q, q, q, q, limit))
        return self._filas_a_models(self.db.fetchall())

    def get_book(self, query: str) -> BookModel:
        """Retorna el primer resultado de una búsqueda por texto."""
        resultados = self.search_books(query, limit=1)
        return resultados[0] if resultados else None

    def get_books_prestados(self) -> list:
        """Retorna todos los libros que están prestados."""
        self.db.execute("SELECT * FROM libros WHERE prestado != 'NO' AND prestado != ''")
        return self._filas_a_models(self.db.fetchall())

    def get_books_donados(self) -> list:
        """Retorna todos los libros donados."""
        self.db.execute("SELECT * FROM libros WHERE donado = 'SI'")
        return self._filas_a_models(self.db.fetchall())

    def get_books_by_categoria(self, categoria: str) -> list:
        """Retorna todos los libros de una categoría."""
        self.db.execute("SELECT * FROM libros WHERE categoria LIKE ?", (f"%{categoria}%",))
        return self._filas_a_models(self.db.fetchall())

    def get_books_by_autor(self, autor: str) -> list:
        """Retorna todos los libros de un autor."""
        self.db.execute("SELECT * FROM libros WHERE autor LIKE ?", (f"%{autor}%",))
        return self._filas_a_models(self.db.fetchall())

    def count_books(self) -> int:
        """Retorna el total de registros en la DB."""
        self.db.execute("SELECT COUNT(*) FROM libros")
        resultado = self.db.fetchone()
        return resultado[0] if resultado else 0

    # -------------------------
    # Escritura
    # -------------------------

    def add_book(self, book: BookModel) -> bool:
        """Inserta un libro en la DB. Retorna True si tuvo éxito."""
        try:
            self.db.execute("""
                INSERT INTO libros 
                    (titulo, categoria, editorial, codigo_ref, codigo_isbn,
                     referencia, cantidad, estado, autor, prestado, donado, fecha)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                book.titulo, book.categoria, book.editorial, book.codigo_ref,
                book.codigo_isbn, book.referencia, book.cantidad, book.estado,
                book.autor, book.prestado, book.donado, book.fecha
            ))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"[BookRepo] Error al agregar libro: {e}")
            return False

    def add_books(self, books: list) -> tuple:
        """
        Inserta una lista de BookModel en la DB de forma masiva.
        Retorna (exitosos, fallidos).
        """
        exitosos = 0
        fallidos = 0
        for book in books:
            if self.add_book(book):
                exitosos += 1
            else:
                fallidos += 1
        return exitosos, fallidos

    def update_book(self, book_id: int, new_book: BookModel) -> bool:
        """
        Actualiza todos los campos de un libro por su ID.
        Retorna True si se modificó algún registro.
        """
        try:
            self.db.execute("""
                UPDATE libros SET
                    titulo      = ?,
                    categoria   = ?,
                    editorial   = ?,
                    codigo_ref  = ?,
                    codigo_isbn = ?,
                    referencia  = ?,
                    cantidad    = ?,
                    estado      = ?,
                    autor       = ?,
                    prestado    = ?,
                    donado      = ?,
                    fecha       = ?
                WHERE id = ?
            """, (
                new_book.titulo, new_book.categoria, new_book.editorial,
                new_book.codigo_ref, new_book.codigo_isbn, new_book.referencia,
                new_book.cantidad, new_book.estado, new_book.autor,
                new_book.prestado, new_book.donado, new_book.fecha,
                book_id
            ))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"[BookRepo] Error al actualizar libro {book_id}: {e}")
            return False

    def update_prestado(self, book_id: int, prestado: str) -> bool:
        """Actualiza solo el campo 'prestado' de un libro."""
        try:
            self.db.execute(
                "UPDATE libros SET prestado = ? WHERE id = ?",
                (prestado, book_id)
            )
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"[BookRepo] Error al actualizar prestado: {e}")
            return False

    def delete_book(self, book_id: int) -> bool:
        """Elimina un libro por su ID. Retorna True si se eliminó."""
        try:
            self.db.execute("DELETE FROM libros WHERE id = ?", (book_id,))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"[BookRepo] Error al eliminar libro {book_id}: {e}")
            return False

    def delete_all_books(self) -> bool:
        """Elimina todos los registros. Útil para reimportar desde cero."""
        try:
            self.db.execute("DELETE FROM libros")
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"[BookRepo] Error al vaciar tabla: {e}")
            return False
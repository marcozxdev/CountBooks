from src.models.bookModel import BookModel
from src.repository.bookRepo import BookRepo
from src.database.database import Database


class BookService:
    def __init__(self, repo: BookRepo):
        self.repo = repo

    # -------------------------
    # Consultas
    # -------------------------

    def get_books(self, quantity: int = None) -> list:
        """Retorna todos los libros o un límite."""
        return self.repo.get_books(quantity)

    def get_book_by_id(self, book_id: int) -> BookModel | None:
        """Retorna un libro por ID, o None si no existe."""
        return self.repo.get_book_by_id(book_id)

    def search_books(self, query: str, limit: int = 10) -> list:
        """Busca libros por texto en los campos principales."""
        if not query or not query.strip():
            return []
        return self.repo.search_books(query.strip(), limit)

    def get_books_prestados(self) -> list:
        """Retorna todos los libros actualmente prestados."""
        return self.repo.get_books_prestados()

    def get_books_perdidos(self) -> list:
        """Retorna todos los libros marcados como perdidos."""
        return self.repo.get_books_perdidos()

    def get_books_by_categoria(self, categoria: str) -> list:
        return self.repo.get_books_by_categoria(categoria)

    def get_books_by_autor(self, autor: str) -> list:
        return self.repo.get_books_by_autor(autor)

    def count_books(self) -> int:
        """Total de registros en el inventario."""
        return self.repo.count_books()

    # -------------------------
    # Agregar libros
    # -------------------------

    def add_book(self, book: BookModel) -> tuple[bool, str]:
        """
        Valida y agrega un libro al inventario.
        Retorna (True, "") si tuvo éxito, o (False, "mensaje de error").
        """
        ok, error = self._validar_libro(book)
        if not ok:
            return False, error

        book = self._normalizar_libro(book)
        guardado = self.repo.add_book(book)

        if not guardado:
            return False, "Error al guardar en la base de datos."
        return True, ""

    def add_books_from_excel(self, libros: list) -> dict:
        """
        Agrega una lista de BookModel proveniente de un Excel.
        Retorna un resumen con exitosos, fallidos y los errores.
        """
        exitosos = 0
        fallidos = []

        for i, libro in enumerate(libros):
            ok, error = self.add_book(libro)
            if ok:
                exitosos += 1
            else:
                fallidos.append({"fila": i + 1, "titulo": libro.titulo, "error": error})

        return {
            "exitosos": exitosos,
            "fallidos": len(fallidos),
            "errores": fallidos,
        }

    # -------------------------
    # Actualizar libros
    # -------------------------

    def update_book(self, book_id: int, new_book: BookModel) -> tuple[bool, str]:
        """Valida y actualiza un libro existente."""
        if not self.repo.get_book_by_id(book_id):
            return False, f"No existe un libro con ID {book_id}."

        ok, error = self._validar_libro(new_book)
        if not ok:
            return False, error

        new_book = self._normalizar_libro(new_book)
        guardado = self.repo.update_book(book_id, new_book)

        if not guardado:
            return False, "Error al actualizar en la base de datos."
        return True, ""

    def prestar_libro(self, book_id: int, nombre_persona: str) -> tuple[bool, str]:
        """
        Marca un libro como prestado a una persona.
        El campo 'prestado' guarda el nombre de quien lo tiene.
        """
        if not nombre_persona or not nombre_persona.strip():
            return False, "Debe indicar el nombre de la persona."

        libro = self.repo.get_book_by_id(book_id)
        if not libro:
            return False, f"No existe un libro con ID {book_id}."

        if libro.prestado and libro.prestado.upper() != "NO":
            return False, f"El libro ya está prestado a '{libro.prestado}'."

        guardado = self.repo.update_prestado(book_id, nombre_persona.strip())
        if not guardado:
            return False, "Error al registrar el préstamo."
        return True, ""

    def devolver_libro(self, book_id: int) -> tuple[bool, str]:
        """Marca un libro como devuelto (prestado = 'NO')."""
        libro = self.repo.get_book_by_id(book_id)
        if not libro:
            return False, f"No existe un libro con ID {book_id}."

        if not libro.prestado or libro.prestado.upper() == "NO":
            return False, "El libro no está registrado como prestado."

        guardado = self.repo.update_prestado(book_id, "NO")
        if not guardado:
            return False, "Error al registrar la devolución."
        return True, ""

    def marcar_perdido(self, book_id: int) -> tuple[bool, str]:
        """Marca un libro como perdido."""
        libro = self.repo.get_book_by_id(book_id)
        if not libro:
            return False, f"No existe un libro con ID {book_id}."

        if getattr(libro, "perdido", "NO").upper() == "SI":
            return False, "El libro ya está marcado como perdido."

        guardado = self.repo.update_perdido(book_id, "SI")
        if not guardado:
            return False, "Error al registrar como perdido."
        return True, ""

    def recuperar_libro(self, book_id: int) -> tuple[bool, str]:
        """Desmarca un libro como perdido."""
        libro = self.repo.get_book_by_id(book_id)
        if not libro:
            return False, f"No existe un libro con ID {book_id}."

        if getattr(libro, "perdido", "NO").upper() != "SI":
            return False, "El libro no está marcado como perdido."

        guardado = self.repo.update_perdido(book_id, "NO")
        if not guardado:
            return False, "Error al actualizar el registro."
        return True, ""

    # -------------------------
    # Eliminar libros
    # -------------------------

    def delete_book(self, book_id: int) -> tuple[bool, str]:
        """Elimina un libro por ID."""
        if not self.repo.get_book_by_id(book_id):
            return False, f"No existe un libro con ID {book_id}."

        eliminado = self.repo.delete_book(book_id)
        if not eliminado:
            return False, "Error al eliminar de la base de datos."
        return True, ""

    def reset_inventario(self) -> tuple[bool, str]:
        """
        Elimina todos los registros. Útil antes de reimportar desde Excel.
        """
        ok = self.repo.delete_all_books()
        if not ok:
            return False, "Error al limpiar el inventario."
        return True, ""

    # -------------------------
    # Helpers privados
    # -------------------------

    def _validar_libro(self, book: BookModel) -> tuple[bool, str]:
        """Valida los campos requeridos y los valores permitidos."""
        if not book.titulo or not book.titulo.strip():
            return False, "El título es obligatorio."

        if not book.autor or not book.autor.strip():
            return False, "El autor es obligatorio."

        if not isinstance(book.cantidad, int) or book.cantidad < 0:
            return False, "La cantidad debe ser un número entero positivo."

        estados_validos = {"BUENO", "MALO", "REGULAR", "DETERIORADO"}
        if book.estado.upper() not in estados_validos:
            return False, f"Estado inválido '{book.estado}'. Opciones: {', '.join(estados_validos)}."

        return True, ""

    def _normalizar_libro(self, book: BookModel) -> BookModel:
        """Limpia espacios y estandariza mayúsculas en campos clave."""
        book.titulo     = book.titulo.strip()
        book.autor      = book.autor.strip()
        book.categoria  = book.categoria.strip() if book.categoria else ""
        book.editorial  = book.editorial.strip() if book.editorial else ""
        book.estado     = book.estado.strip().upper()
        book.prestado   = book.prestado.strip().upper() if book.prestado else "NO"
        book.donado     = book.donado.strip().upper() if book.donado else "NO"
        book.perdido    = getattr(book, "perdido", "NO")
        if book.perdido:
            book.perdido = book.perdido.strip().upper()
        else:
            book.perdido = "NO"
        return book


class BookModel:
    def __init__(
        self,
        titulo: str="", 
        categoria: str="",
        editorial: str="",
        codigo_ref: str="", 
        codigo_isbn: str="",
        referencia: str="", 
        cantidad: int=1, 
        estado: str="BUENO", 
        autor: str="", 
        prestado: str="NO", 
        donado: str="NO", 
        fecha: str="",
        perdido: str="NO"
        ):

        self.titulo = titulo
        self.categoria = categoria
        self.editorial = editorial
        self.codigo_ref = codigo_ref
        self.codigo_isbn = codigo_isbn
        self.referencia = referencia
        self.cantidad = cantidad
        self.estado = estado
        self.autor = autor
        self.prestado = prestado
        self.donado = donado
        self.fecha = fecha
        self.perdido = perdido
        self.id: int = None

    def a_book(self):
        book = {"titulo": self.titulo, "categoria": self.categoria, "editorial": self.editorial,
                "codigo_ref": self.codigo_ref,"codigo_isbn": self.codigo_isbn, "referencia": self.referencia, "cantidad": self.cantidad, "estado": self.estado, 
                "autor": self.autor, "prestado": self.prestado, "donado": self.donado, "fecha": self.fecha, "perdido": self.perdido, "id": self.id }
        return book        

    




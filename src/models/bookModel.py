

class BookModel:
    def __init__(self, titulo: str, categoria: str, editorial: str, codigo: str, referencia: str, cantidad: int, estado: str, autor: str, prestado: str, donado: str, fecha: str):

        self.titulo = titulo
        self.categoria = categoria
        self.editorial = editorial
        self.codigo = codigo
        self.referencia = referencia
        self.cantidad = cantidad
        self.estado = estado
        self.autor = autor
        self.prestado = prestado
        self.donado = donado
        self.fecha = fecha
        self.id: int

    def a_book(self):
        book = {"titulo": self.titulo, "categoria": self.categoria, "editorial": self.editorial,
                "codigo": self.codigo, "referencia": self.referencia, "cantidad": self.cantidad, "estado": self.estado, 
                "autor": self.autor, "prestado": self.prestado, "donado": self.donado, "fecha": self.fecha, "id": self.id }
        return book        

    




from pathlib import Path # Importamos la librería pathlib
import sqlite3 #Importamos la librería sqlite3 y la renombramos con "as" para personalizar el nombre a uno más corto y cómodo.

def get_db_path(): # Declaramos una función llamada "get_db_path" para obtener la ruta en dónde nuestra base de datos (DB) se almacenará. 
    app_dir = Path.home() / ".books" # Declaramos una variable llamada "app_dir" para almacenar el objeto "home" del submódulo "Path".
    app_dir.mkdir(exist_ok=True) # Accedemos al método mkdir del objeto home para crear directorios.
    return app_dir / "books.db" # Retornamos la variable app_dir dividida por el string "books.db" que será la BBDD (Base de datos)


DB_PATH = get_db_path() # Definimos una variable con nomenclatura de constante llamada "DB_PATH" para guardar el valor de retorno al llamar a la función "get_db_path" y obtener la ruta dónde gestionaremos la ubicación de nuestra BBDD (Base de datos).


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def debug_characters(self, value):
        FORBIDDEN_CHARACTERS = ("-", ";", "_", "(", ")", "+", "'")
        self.danger = False

        for i in value:
            for j in FORBIDDEN_CHARACTERS:
                if i == j:
                    self.danger = True
    
    # ==========================
    #     Métodos Básicos
    # ==========================

    def execute(self, query, params=None):
        if params is None:
            params = ()

        self.debug_characters(query)

        if self.danger:
            print("El usuario está ingresando carácteres especiales en el campo.")

            raise ValueError("Protect DB: No se permiten carácteres especiales.") # Se debe manejar la excepción o si no la app colapsará
        else:
            self.cursor.execute(query, params)


    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()


# Estructura de la base de datos donde se define sus relaciones y sus camps 

def estructure_db(database: Database):
    cursor = database.cursor

    # Usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        categoria TEXT,
        editorial TEXT ,
        codigo TEXT,
        referencia TEXT,
        cantidad INTEGER NOT NULL,
        estado TEXT,
        autor TEXT,
        prestado TEXT,
        donado TEXT,
        fecha TEXT
    )
    """)


    database.commit()


# =========================
# Inicialización Automática
# =========================
def init_db():
    if not DB_PATH.exists():
        DB_PATH.touch()

    db = Database(DB_PATH)
    estructure_db(db)
    return db


# Instancia lista para usar
db = init_db()

# print(get_db_path())

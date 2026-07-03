from pathlib import Path # Importamos el submódulo u objeto Path de la librería pathlib para navegar por las rutas y ejecutar comandos.
import sqlite3 # Importamos la librería sqlite3 del motor SQLite3 para diseñar y administrar bases de datos locales.


def get_db_path():
    """
    Determina y crea la ruta del archivo de la base de datos.
    Crea un directorio oculto '.books' en el Home del usuario si no existe.
    """
    app_dir = Path.home() / ".books"
    app_dir.mkdir(exist_ok=True)
    return app_dir / "books.db"


# Ruta global donde se almacenará de forma definitiva la base de datos
DB_PATH = get_db_path()



class Database:
    """
    Clase controladora para gestionar la conexión, configuración
    y operaciones básicas sobre la base de datos SQLite3.
    """
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

        # Establece la conexión permitiendo que sea compartida entre hilos (threads)
        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        """
        Posible AttributeError: El objeto conn no tiene el acceso directo al método 'execute()'.
        Solución: Inicializar el método 'cursor()' para que se inicializen los subsistemas y devuelva un objeto para finalmente acceder al método 'execute()'.
        Ejemplo:
        
        self.cursor = self.conn.cursor()
        self.cursor.execute(const string instruction)
        """
        
        # Configuraciones PRAGMA para optimizar el rendimiento de SQLite3
        self.conn.execute("PRAGMA journal_mode=WAL") # Registros de escritura por adelantado (concurrencia)
        self.conn.execute("PRAGMA synchronous=NORMAL") # Reduce las sincronizaciones a disco para ganar velocidad
        self.conn.execute("PRAGMA temp_store=MEMORY") # Almacena tablas/índices temporales en la memoria RAM
        self.conn.execute("PRAGMA cache_size=-10000") # Asigna aprox. 10MB de memoria caché para la base de datos

        # Crea el cursor para ejecutar sentencias SQL
        self.cursor = self.conn.cursor()

    # -------------------------
    #    Métodos Básicos
    # -------------------------

    def execute(self, query, params=None):
        """Ejecuta una consulta SQL con o sin parámetros."""
        if params is None:
            params = ()

        # CVE Detected!: SQL Inyection - A03:2021-Injection
        
        self.cursor.execute(query, params)

    def fetchone(self):
        """Recupera la siguiente fila de un resultado de consulta."""
        return self.cursor.fetchone()

    def fetchall(self):
        """Recupera todas las filas restantes de un resultado de consulta."""
        return self.cursor.fetchall()

    def commit(self):
        """Guarda permanentemente los cambios de la transacción actual en el disco."""
        self.conn.commit()

    def rollback(self):
        """Revierte los cambios de la transacción actual en caso de error."""
        self.conn.rollback()

    def clear_conn(self):
        """Cierra la conexión con el archivo de la base de datos."""
        self.conn.close()


# Estructura de la base de datos
def structure_db(database: Database):
    """
    Crea la tabla 'libros' y sus respectivos índices de búsqueda rápida
    si no existen previamente en la base de datos.
    """
    cursor = database.cursor

    # -------------------------
    #     Tabla libros
    # -------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        categoria TEXT,
        editorial TEXT,
        codigo_ref TEXT,
        codigo_isbn TEXT,
        referencia TEXT,
        cantidad INTEGER NOT NULL,
        estado TEXT,
        autor TEXT,
        prestado TEXT,
        donado TEXT,
        fecha TEXT,
        perdido TEXT
    )
    """)

    # -------------------------
    # Índices Para Búsquedas Rápidas
    # -------------------------
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_titulo
    ON libros(titulo)
    """)
    
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_autor
    ON libros(autor)
    """)
    
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_categoria
    ON libros(categoria)
    """)
    
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_isbn
    ON libros(codigo_isbn)
    """)

    # Confirma la creación de las tablas e índices
    database.commit()


# -------------------------
# Inicialización Automática
# -------------------------

def init_db():
    """
    Inicializa el entorno: asegura la existencia del archivo físico,
    instancia la clase de conexión y genera la estructura base.
    """
    if not DB_PATH.exists():
        DB_PATH.touch()

    db = Database(DB_PATH)
    structure_db(db)

    return db


# Instancia lista para usar
db = init_db()

from pathlib import Path
import sqlite3


def get_db_path():
    app_dir = Path.home() / ".books"
    app_dir.mkdir(exist_ok=True)
    return app_dir / "books.db"


DB_PATH = get_db_path()



class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA temp_store=MEMORY")
        self.conn.execute("PRAGMA cache_size=-10000")

        self.cursor = self.conn.cursor()

    # -------------------------
    # Métodos básicos
    # -------------------------

    def execute(self, query, params=None):
        if params is None:
            params = ()

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


# estructura de la base de datos
def estructure_db(database: Database):
    cursor = database.cursor

    # -------------------------
    # Tabla libros
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
    # Índices para búsquedas rápidas
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

    database.commit()


# -------------------------
# Inicialización automática
# -------------------------

def init_db():
    if not DB_PATH.exists():
        DB_PATH.touch()

    db = Database(DB_PATH)
    estructure_db(db)

    return db


# instancia lista para usar
db = init_db()
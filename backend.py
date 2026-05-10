from fastapi import FastAPI # Importamos la librería FastAPI para diseñar APIs y servidores backend
from fastapi import HTMLResponse # De la librería FastAPI importamos HTMLResponse para dar respuestas en HTML
from fastapi import HTTPException # De la librería FastAPI importamos HTTPException para lanzar excepciones y proporcionar información al usuario acerca del error
from fastapi.middleware.cors import CORSMiddleware # De la librería FastAPI importamos CORSMiddleware para agregarlo al middleware de la app
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND # De la librería starlette importamos HTTP_403_FORBIDDEN y HTTP_404_NOT_FOUND para prohibir el acesso al un usuario en específico e informar si una URL, endpoint o dato no existe o no se encuentra
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR # De la librería starlette importamos la HTTP_200_Ok y HTTP_500_INTERNAL_SERVER&_ERROR para informar si la petición del usuario ha sido procesada y devuelto un resultado con éxito o se ha producido un error interno del servidor

class DataBase:
    def __init__(self):
        try:
            self.DB_NAME = "data_server.db"
            self.conn = sql.connect(self.DB_NAME)
        finally:
            self.conn.commit()
            self.conn.close()

        self.create_table()

    def create_table(self):
        try:
            self.conn = sql.connect(self.DB_NAME)
            self.cursor = self.conn.cursor()
            self.cursor.execute(
              """CREATE TABLE IF NOT EXISTS books(
                   name_book TEXT,
                   title TEXT,
                   model TEXT,
                   autor TEXT,
                   book TEXT
                )"""
            )
        finally:
            self.conn.commit()
            self.conn.close()

    def db_protection(self, data_users):
        FORBIDDEN_CHARACTERS = ["-", "_", "*", "(", ")", "#", "'", '"', ";", ":", "+", "{", "}"]
        COMMANDS_FORBIDDEN = ["SELECT", "FROM", "UPDATE", "DROP", "DELETE", "UNION", "SET", "INSERT"]
        self.is_secure = True
        self.is_danger = False
        
        for i in FORBIDDEN_CHARACTERS:
            for j in data_users:
                if j == i:
                    self.is_secure = False
                    break
                
    
    def insert_data(self, QUERY_SQL, data_users):
        try:
            self.conn = sql.connect(self.DB_NAME)
            self.cursor = self.conn.cursor()

            scan_data_users = self.db_protection(data_user)

            if is_secure:
                self.cursor.execute(QUERY_SQL) # Critical Vulnerability: SQL Inyection
        finally:
            self.conn.commit()
            self.conn.close()

class InputData:
    user_name: str
    psswd: str

app = FastAPI()
app.title("System Books API backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/home', tags=["Home"])
def home():
    content_html = """
        <!DOCTYPE html>
          <html lang="es">
            <head>
              <title>Home</title>
                <meta charset="utf-8">
                  <meta name="description" content="This is a frontend de start. Is the home">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <!-- <link rel="stylesheet" href="style.css"> -->
            </head>
            <body>
              <h1>Welcome to home</h1>
            </body>
          </html>
    """
    
    HTMLResponse(
        content=content_html
        status=HTTP_200_OK
    )
  
    return {"status": "200"}

@app.post('/login', tags=["Login"])
def login(user_name: InputData, psswd: InputData):
    # db = DataBase()
  
    return {"status": "201"}

@app.get('/books', tags=["Books"])
def get_books():
    # db = DataBase()
  
    return {
      "status": "200",
      "books": "book" # En mantenimiento
    }

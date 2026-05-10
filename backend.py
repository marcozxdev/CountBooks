from fastapi import FastAPI
from fastapi import HTMLResponse # Error: Se corregirá

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
    
    def insert_data(self, QUERY_SQL):
        try:
            self.conn = sql.connect(self.DB_NAME)
            self.cursor = self.conn.cursor()
            self.cursor.execute(QUERY_SQL) # Critical Vulnerability: SQL Inyection
        finally:
            self.conn.commit()
            self.conn.close()

class InputData:
    user_name: str
    psswd: str

app = FastAPI()
app.title("System Books API backend")

@app.get('/home', tags=["Home"])
def home():
    HTMLResponse
  
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

from fastapi import FastAPI

class DataBase:
    def __init__(self):
        pass

app = FastAPI()
app.title("System Books API backend")

@app.get('/home', tags=["Home"])
def home():
    # HTML
  
    return {"status": "200"}

@app.post('/login', tags=["Login"])
def login(user_name: str, psswd: str):
    # db = DataBase()
  
    return {"status": "201"}

@app.get('/books', tags=["Books"])
def get_books():
    # db = DataBase()
  
    return {
      "status": "200",
      "books": "book" # En mantenimiento
    }

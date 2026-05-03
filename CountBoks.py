""" este es el ejecutable de la app """
from src.ui.main_window import run_app
from src.services.bookServices import BookService
from src.repository.bookRepo import BookRepo
from src.database.database import db

run_app(service=BookService(BookRepo(db), db))
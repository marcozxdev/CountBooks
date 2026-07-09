""" Este es el ejecutable de la app """
from src.ui.main_window import run_app # Importamos el submódulo que posee la UI para proyectar la Interfaz Gráfica a la Main App.
from src.services.bookServices import BookService
from src.repository.bookRepo import BookRepo
from src.database.database import db # Importamos el submódulo estructurado de la app para la interacción con el motor SQLite3 y bases de datos.
import requests # Importamos la librería requests para realizar peticiones a serviores y APIs.

run_app(service=BookService(BookRepo(db)))


########## Contribuido por: ##########
# - Marcozxdev Github:https://github.com/marcozxdev
# - Jhosepthehacker Github:https://github.com/Jhosepthehacker
# - Y herramientas de inteligencia artificial como ChatGPT, Claude y  Github Copilot para el diseño y creación de la UI



"""Creado con el propósito de el manejo eficiente de los inventarios de libros, permitiendo a los usuarios contar y gestionar sus colecciones de manera sencilla y organizada. Con esta aplicación, los usuarios pueden mantener un registro actualizado de sus libros, facilitando la organización y el acceso a su biblioteca personal.
pensado en ser gratis y de código abierto para que cualquier persona pueda contribuir y mejorar la aplicación, fomentando una comunidad activa de desarrolladores y entusiastas de los libros. Con esta iniciativa, se busca crear una herramienta útil y accesible para todos los amantes de la lectura, promoviendo la colaboración y el intercambio de conocimientos en el ámbito de la gestión de bibliotecas personales.
"""

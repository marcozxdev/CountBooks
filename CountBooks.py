""" este es el ejecutable de la app """
from src.ui.main_window import run_app
from src.services.bookServices import BookService
from src.repository.bookRepo import BookRepo
from src.database.database import db

run_app(service=BookService(BookRepo(db)))


########## contribuido por: ##########
# - marcozxdev Github:https://github.com/marcozxdev
# - Jhosepthehacker Github:https://github.com/Jhosepthehacker
# - y herramientas de inteligencia artificial como ChatGPT, Claude y  Github Copilot para el diseño y creacion de la Ui 



"""creado con el proposito de el manejo eficiente de los inventarios de libros, permitiendo a los usuarios contar y gestionar sus colecciones de manera sencilla y organizada. Con esta aplicación, los usuarios pueden mantener un registro actualizado de sus libros, facilitando la organización y el acceso a su biblioteca personal.
pensado en ser gratis y de codigo abierto para que cualquier persona pueda contribuir y mejorar la aplicación, fomentando una comunidad activa de desarrolladores y entusiastas de los libros. Con esta iniciativa, se busca crear una herramienta útil y accesible para todos los amantes de la lectura, promoviendo la colaboración y el intercambio de conocimientos en el ámbito de la gestión de bibliotecas personales.
"""

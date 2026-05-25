import pyside6 # Importamos la librería pyside6 para la UI gráfica (GUI).
import requests
import src.database.database.py as sql

""" Este es el ejecutable de la app """

headers = {}

body = {}

data = requests.get("https://example.render")
data.json()

from fastapi import FastAPI # Importamos la librería FastAPI para diseñar APIs y servidores backend
from fastapi import HTMLResponse # De la librería FastAPI importamos HTMLResponse para dar respuestas en HTML
from fastapi import HTTPException # De la librería FastAPI importamos HTTPException para lanzar excepciones y proporcionar información al usuario acerca del error
from fastapi.middleware.cors import CORSMiddleware # De la librería FastAPI importamos CORSMiddleware para agregarlo al middleware de la app
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND # De la librería starlette importamos HTTP_403_FORBIDDEN y HTTP_404_NOT_FOUND para prohibir el acesso al un usuario en específico e informar si una URL, endpoint o dato no existe o no se encuentra
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR # De la librería starlette importamos la HTTP_200_Ok y HTTP_500_INTERNAL_SERVER_ERROR para informar si la petición del usuario ha sido procesada y devuelto un resultado con éxito o se ha producido un error interno del servidor

# ========================
#      Base de datos
# ========================

# Definición de la clase DataBase para gestionar la persistencia de datos con SQLite
class DataBase:
    # Método constructor que inicializa la configuración de la base de datos
    def __init__(self):
        try:
            self.DB_NAME = "data_server.db" # Definición del nombre del archivo de la base de datos local
            self.conn = sql.connect(self.DB_NAME) # Intento de establecer conexión inicial con el motor SQLite
        finally:
            self.conn.commit() # Asegura que cualquier cambio pendiente se guarde antes de cerrar
            self.conn.close() # Cierre preventivo de la conexión para liberar el recurso del sistema

        self.create_table() # Llamada automática al método de creación de tablas al instanciar la clase

    # Método encargado de definir la estructura de la tabla de inventario
    def create_table(self):
        try:
            self.conn = sql.connect(self.DB_NAME) # Apertura de conexión para realizar operaciones de Definición de Datos (DDL)
            self.cursor = self.conn.cursor() # Creación de un objeto cursor para ejecutar sentencias SQL
            # Ejecución de sentencia SQL para crear la tabla 'books' si no existe previamente
            self.cursor.execute(
              """CREATE TABLE IF NOT EXISTS books(
                   name_book TEXT,
                   title TEXT,
                   model TEXT,
                   autor TEXT,
                   book LONGBLOG
                )"""
            )
        finally:
            self.conn.commit() # Confirmación de la creación de la tabla en el archivo físico
            self.conn.close() # Cierre de la conexión tras completar la operación de estructura

    # Método de seguridad para validar que las entradas del usuario no contengan caracteres sospechosos
    def db_protection(self, data_users):
        # Lista de caracteres especiales comúnmente usados en ataques de inyección SQL
        FORBIDDEN_CHARACTERS = ["-", "_", "*", "(", ")", "#", "'", '"', ";", ":", "+", "{", "}"]
        # Lista de palabras clave de SQL que podrían ser usadas para manipular la base de datos
        COMMANDS_FORBIDDEN = ["SELECT", "FROM", "UPDATE", "DROP", "DELETE", "UNION", "SET", "INSERT"]
        self.is_secure = True # Flag inicial que asume que la entrada es segura
        self.is_danger = False # Flag auxiliar para identificar riesgos detectados
        
        # Bucle anidado para comparar cada carácter prohibido con cada dato ingresado por el usuario
        for i in FORBIDDEN_CHARACTERS:
            for j in data_users:
                if j == i:
                    self.is_secure = False # Si encuentra una coincidencia, marca la entrada como no segura
                    break # Rompe el ciclo interno al encontrar la primera amenaza
                
    # Método para realizar la inserción de nuevos registros de libros en la base de datos
    def insert_data(self, QUERY_SQL, data_users):
        try:
            self.conn = sql.connect(self.DB_NAME) # Apertura de conexión para operación de inserción
            self.cursor = self.conn.cursor() # Inicialización del cursor para la transacción

            # Llamada al método de protección para escanear los datos antes de procesar la consulta
            scan_data_users = self.db_protection(data_user)

            # Validación del flag de seguridad antes de proceder con la ejecución del SQL
            if is_secure:
                self.cursor.execute(QUERY_SQL) # Ejecución de la consulta (Nota: Identificado como punto crítico de vulnerabilidad)
        finally:
            self.conn.commit() # Persistencia de los datos insertados
            self.conn.close() # Cierre de conexión para mantener la integridad del archivo DB

# Clase para definir el esquema de datos esperado en las peticiones de entrada
class InputData:
    user_name: str # Atributo esperado para el nombre de usuario o identificador
    psswd: str # Atributo esperado para la contraseña o clave de acceso

# Inicialización de la aplicación FastAPI
app = FastAPI()
app.title("System Books API backend") # Asignación de un título personalizado a la documentación automática (Swagger)

# Configuración de CORS (Cross-Origin Resource Sharing) para permitir peticiones desde otros dominios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite el acceso desde cualquier origen (ajustar en producción por seguridad)
    allow_credentials=True, # Permite el intercambio de cookies o credenciales en las peticiones
    allow_methods=["*"], # Habilita todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"] # Permite todos los encabezados HTTP personalizados
)

# Definición de la ruta raíz o inicio del sistema de inventario
@app.get('/home', tags=["Home"])
def home():
    # Variable que contiene la estructura HTML de la página de bienvenida
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
    
    # Preparación de la respuesta en formato HTML con código de estado exitoso
    HTMLResponse(
        content=content_html
        status=HTTP_200_OK
    )
  
    # Retorno de un objeto JSON confirmando el estado de la petición
    return {"status": "200"}

# Definición de la ruta para el proceso de autenticación de usuarios
@app.post('/login', tags=["Login"])
def login(user_name: InputData, psswd: InputData):
    # Instanciación comentada de la base de datos (Fase de mantenimiento)
    # db = DataBase()
  
    # Retorno de confirmación de creación de sesión o recepción de datos exitosa
    return {"status": "201"}

# Definición de la ruta para consultar el inventario de libros
@app.get('/books', tags=["Books"])
def get_books():
    # Instanciación comentada de la base de datos para consulta de registros
    # db = DataBase()
  
    # Retorno de la lista de libros (Actualmente en mantenimiento técnico)
    return {
      "status": "200",
      "books": "book" # Placeholder para la futura lista de objetos de libros
}
    

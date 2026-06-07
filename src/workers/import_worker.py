from PySide6.QtCore import QObject, Signal

from src.utils.excel import leer_excel


class ImportWorker(QObject):
    """
    Trabajador en segundo plano encargado de procesar la lectura de archivos Excel
    de forma asíncrona para no congelar la interfaz gráfica de usuario (GUI).
    """

    # Señal que se emite al finalizar con éxito; transporta la lista de libros procesados
    finished = Signal(list)
    # Señal que se emite si ocurre un fallo; transporta el mensaje de error en texto
    error = Signal(str)

    def __init__(self, ruta_excel):
        # Inicializa la clase base QObject para habilitar el soporte de señales
        super().__init__()
        # Almacena la ubicación del archivo Excel que se va a procesar
        self.ruta_excel = ruta_excel

    def run(self):
        """
        Método principal de ejecución del worker. 
        Contiene la lógica pesada que se ejecutará en el hilo secundario.
        """
        try:
            # Intenta realizar la lectura y extracción de los datos del Excel
            libros = leer_excel(self.ruta_excel)

            # Notifica a la interfaz que el proceso terminó enviando los datos
            self.finished.emit(libros)

        except Exception as e:
            # Captura cualquier error (archivo no encontrado, formato inválido, etc.)
            # y envía el mensaje de error detallado a la interfaz
            self.error.emit(str(e))

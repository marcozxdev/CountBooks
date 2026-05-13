from PySide6.QtCore import QObject, Signal

from src.utils.excel import leer_excel


class ImportWorker(QObject):

    finished = Signal(list)
    error = Signal(str)

    def __init__(self, ruta_excel):
        super().__init__()
        self.ruta_excel = ruta_excel

    def run(self):
        try:
            libros = leer_excel(self.ruta_excel)

            self.finished.emit(libros)

        except Exception as e:
            self.error.emit(str(e))
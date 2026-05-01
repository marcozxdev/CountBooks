# src/utils/excel_reader.py
import pandas as pd
from src.models.bookModel import BookModel


# nombres del Excel de la biblioteca -> nombres del modelo
MAPEO_COLUMNAS = {
    "COLECCIÓN DE REFERENCIA"          : "titulo",
    "CARACTERISTICAS DE LA REFERENCIA" : "categoria",
    "EDITORIAL"                        : "editorial",
    "CODIGO"                           : "codigo_ref",
    "REFERENCIA"                       : "referencia",
    "CANTIDAD"                         : "cantidad",
    "ESTADO"                           : "estado",
    "AUTOR"                            : "autor",
    "CODIGO ISBN"                      : "codigo_isbn",
    "PRESTADO"                         : "prestado",
    "DONADO"                           : "donado",
    "FECHA"                            : "fecha",
}

# columnas de la DB — si el Excel las tiene tal cual no necesita mapeo
COLUMNAS_DB = [
    "titulo", "categoria", "editorial", "codigo_ref", "codigo_isbn",
    "referencia", "cantidad", "estado", "autor", "prestado", "donado", "fecha"
]

# requeridas según el tipo de Excel
COLUMNAS_REQUERIDAS = [
    "COLECCIÓN DE REFERENCIA", "CANTIDAD", "AUTOR"
]

COLUMNAS_REQUERIDAS_DB = [
    "titulo", "cantidad", "autor"
]


def _detectar_tipo(df: pd.DataFrame) -> str:
    """
    Detecta si el Excel tiene columnas de la DB o de la biblioteca.
    Retorna 'db' o 'biblioteca'.
    """
    columnas = df.columns.tolist()

    # si tiene al menos las requeridas de la DB, es un Excel de DB
    requeridas_db_presentes = all(col in columnas for col in COLUMNAS_REQUERIDAS_DB)
    if requeridas_db_presentes:
        return "db"

    return "biblioteca"


def validar_columnas(df: pd.DataFrame, requeridas: list) -> list:
    """
    Retorna lista de columnas faltantes — si está vacía, todo bien.
    """
    faltantes = []
    for col in requeridas:
        if col not in df.columns.tolist():
            faltantes.append(col)
    return faltantes


def _get(fila, columna: str, default):
    """
    Obtiene el valor de una columna de forma segura.
    Si no existe o está vacía retorna el valor por defecto.
    """
    if columna not in fila.index:
        return default
    valor = fila[columna]
    if pd.isna(valor) or str(valor).strip() == "":
        return default
    return valor


def _filas_a_libros(df: pd.DataFrame) -> list:
    """
    Convierte las filas del DataFrame en BookModel.
    Se usa después de que las columnas ya están en el formato del modelo.
    """
    libros = []
    for _, fila in df.iterrows():
        libro = BookModel(
            titulo      = str(_get(fila, "titulo",      "")),
            autor       = str(_get(fila, "autor",       "")),
            cantidad    = int(_get(fila, "cantidad",    1)),
            categoria   = str(_get(fila, "categoria",   "")),
            editorial   = str(_get(fila, "editorial",   "")),
            codigo_ref  = str(_get(fila, "codigo_ref",  "")),
            referencia  = str(_get(fila, "referencia",  "")),
            estado      = str(_get(fila, "estado",      "BUENO")),
            codigo_isbn = str(_get(fila, "codigo_isbn", "")),
            prestado    = str(_get(fila, "prestado",    "NO")),
            donado      = str(_get(fila, "donado",      "NO")),
            fecha       = str(_get(fila, "fecha",       "")),
        )
        libros.append(libro)
    return libros


def leer_excel(ruta: str) -> list:
    """
    Lee un Excel y detecta automáticamente su estructura.
    - Si tiene columnas de la DB las usa directamente sin mapear.
    - Si tiene columnas de la biblioteca las mapea al modelo.
    """
    df = pd.read_excel(ruta)
    df.columns = df.columns.str.strip()

    tipo = _detectar_tipo(df)

    if tipo == "db":
        # columnas ya tienen el mismo nombre que el modelo — solo validar
        faltantes = validar_columnas(df, COLUMNAS_REQUERIDAS_DB)
        if faltantes:
            raise ValueError(f"El Excel no tiene las columnas requeridas: {faltantes}")

    else:
        # columnas tienen nombres de la biblioteca — validar y mapear
        faltantes = validar_columnas(df, COLUMNAS_REQUERIDAS)
        if faltantes:
            raise ValueError(f"El Excel no tiene las columnas requeridas: {faltantes}")
        df = df.rename(columns=MAPEO_COLUMNAS)

    return _filas_a_libros(df)


def exportar_excel(libros: list, ruta: str) -> None:
    """
    Exporta una lista de BookModel a Excel con los nombres de la DB.
    Este Excel puede reimportarse directamente con leer_excel().
    """
    filas = []
    for libro in libros:
        filas.append({
            "titulo"      : libro.titulo,
            "categoria"   : libro.categoria,
            "editorial"   : libro.editorial,
            "codigo_ref"  : libro.codigo_ref,
            "codigo_isbn" : libro.codigo_isbn,
            "referencia"  : libro.referencia,
            "cantidad"    : libro.cantidad,
            "estado"      : libro.estado,
            "autor"       : libro.autor,
            "prestado"    : libro.prestado,
            "donado"      : libro.donado,
            "fecha"       : libro.fecha,
        })

    df = pd.DataFrame(filas)
    df.to_excel(ruta, index=False)

# print(leer_excel("docs/INVENTARIO GAB - 2023.xlsx"))




# df = pd.read_excel("docs/INVENTARIO GAB - 2023.xlsx")
# print(df.columns.tolist())  # imprime los nombres exactos de las columnas
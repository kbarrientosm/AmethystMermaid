
import oracledb
from app.database.conexion import obtener_conexion


def listar_categorias():
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)
        cursor.callproc("PR_LISTAR_CATEGORIAS", [resultado])

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        filas = cursor_resultado.fetchall()

        categorias = [
            dict(zip(columnas, fila))
            for fila in filas
        ]

        return categorias

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def buscar_categoria(id_categoria):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_CATEGORIA",
            [id_categoria, resultado]
        )

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        fila = cursor_resultado.fetchone()

        if fila is None:
            return None

        categoria = dict(zip(columnas, fila))

        return categoria

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def registrar_categoria(nombre):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        id_categoria = cursor.var(oracledb.NUMBER)

        cursor.callproc(
            "PR_REGISTRAR_CATEGORIA",
            [nombre, id_categoria]
        )

        conexion.commit()

        return int(id_categoria.getvalue())

    except Exception:
        if conexion is not None:
            conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def actualizar_categoria(id_categoria, nombre):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_CATEGORIA",
            [id_categoria, nombre]
        )

        conexion.commit()

    except Exception:
        if conexion is not None:
            conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()


def eliminar_categoria(id_categoria):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_CATEGORIA",
            [id_categoria]
        )

        conexion.commit()

    except Exception:
        if conexion is not None:
            conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

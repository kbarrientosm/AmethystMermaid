
import oracledb
from app.database.conexion import obtener_conexion


def listar_roles():
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc("PR_LISTAR_ROLES", [resultado])

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        filas = cursor_resultado.fetchall()

        roles = [
            dict(zip(columnas, fila))
            for fila in filas
        ]

        return roles

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def buscar_rol(id_rol):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_ROL",
            [id_rol, resultado]
        )

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        fila = cursor_resultado.fetchone()

        if fila is None:
            return None

        return dict(zip(columnas, fila))

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def registrar_rol(nombre, descripcion):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        id_rol = cursor.var(oracledb.NUMBER)

        cursor.callproc(
            "PR_REGISTRAR_ROL",
            [nombre, descripcion, id_rol]
        )

        conexion.commit()

        return int(id_rol.getvalue())

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def actualizar_rol(id_rol, nombre, descripcion):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_ROL",
            [id_rol, nombre, descripcion]
        )

        conexion.commit()

        return True

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def eliminar_rol(id_rol):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_ROL",
            [id_rol]
        )

        conexion.commit()

        return True

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()

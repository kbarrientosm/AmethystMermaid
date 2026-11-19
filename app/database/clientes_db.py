
import oracledb

from app.database.conexion import obtener_conexion


def listar_clientes():
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_LISTAR_CLIENTES",
            [resultado]
        )

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        filas = cursor_resultado.fetchall()

        clientes = [
            dict(zip(columnas, fila))
            for fila in filas
        ]

        return clientes

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def buscar_cliente(id_cliente):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_CLIENTE",
            [id_cliente, resultado]
        )

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        fila = cursor_resultado.fetchone()

        if fila is None:
            return None

        cliente = dict(zip(columnas, fila))

        return cliente

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def registrar_cliente(nombre, correo, telefono, direccion):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        id_cliente = cursor.var(oracledb.NUMBER)

        cursor.callproc(
            "PR_REGISTRAR_CLIENTE",
            [
                nombre,
                correo,
                telefono,
                direccion,
                id_cliente
            ]
        )

        conexion.commit()

        return int(id_cliente.getvalue())

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def actualizar_cliente(
    id_cliente,
    nombre,
    correo,
    telefono,
    direccion
):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_CLIENTE",
            [
                id_cliente,
                nombre,
                correo,
                telefono,
                direccion
            ]
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


def eliminar_cliente(id_cliente):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_CLIENTE",
            [id_cliente]
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

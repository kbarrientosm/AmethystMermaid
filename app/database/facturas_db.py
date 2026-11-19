
import oracledb

from app.database.conexion import obtener_conexion


def listar_facturas():
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_LISTAR_FACTURAS",
            [resultado]
        )

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        filas = cursor_resultado.fetchall()

        return [
            dict(zip(columnas, fila))
            for fila in filas
        ]

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def buscar_factura(id_factura):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_FACTURA",
            [id_factura, resultado]
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


def registrar_factura(id_venta, subtotal, impuesto):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        id_nueva_factura = cursor.var(oracledb.NUMBER)

        cursor.callproc(
            "PR_REGISTRAR_FACTURA",
            [
                id_venta,
                subtotal,
                impuesto,
                id_nueva_factura
            ]
        )

        conexion.commit()

        return int(id_nueva_factura.getvalue())

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def actualizar_factura(id_factura, subtotal, impuesto):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_FACTURA",
            [
                id_factura,
                subtotal,
                impuesto
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


def eliminar_factura(id_factura):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_FACTURA",
            [id_factura]
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

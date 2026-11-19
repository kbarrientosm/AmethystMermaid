
import oracledb

from app.database.conexion import obtener_conexion


def listar_detalles_venta(id_venta):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_LISTAR_DETALLES_VENTA",
            [id_venta, resultado]
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


def buscar_detalle_venta(id_detalle):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_DETALLE_VENTA",
            [id_detalle, resultado]
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


def registrar_detalle_venta(
    id_venta,
    id_producto,
    cantidad,
    precio_unitario
):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        id_nuevo_detalle = cursor.var(oracledb.NUMBER)

        cursor.callproc(
            "PR_REGISTRAR_DETALLE_VENTA",
            [
                id_venta,
                id_producto,
                cantidad,
                precio_unitario,
                id_nuevo_detalle
            ]
        )

        conexion.commit()

        return int(id_nuevo_detalle.getvalue())

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def actualizar_detalle_venta(
    id_detalle,
    id_producto,
    cantidad,
    precio_unitario
):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_DETALLE_VENTA",
            [
                id_detalle,
                id_producto,
                cantidad,
                precio_unitario
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


def eliminar_detalle_venta(id_detalle):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_DETALLE_VENTA",
            [id_detalle]
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

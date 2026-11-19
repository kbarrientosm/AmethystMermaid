
import oracledb

from app.database.conexion import obtener_conexion


def _convertir_resultados(cursor, resultados):
    columnas = [columna[0].lower() for columna in cursor.description]

    return [
        dict(zip(columnas, fila))
        for fila in resultados
    ]


def listar_movimientos():
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_LISTAR_MOVIMIENTOS",
            [resultado]
        )

        cursor_resultado = resultado.getvalue()

        registros = cursor_resultado.fetchall()

        return _convertir_resultados(cursor_resultado, registros)

    except Exception:
        if conexion:
            conexion.rollback()
        raise

    finally:
        if cursor_resultado:
            cursor_resultado.close()

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()


def buscar_movimiento(id_movimiento):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_MOVIMIENTO",
            [id_movimiento, resultado]
        )

        cursor_resultado = resultado.getvalue()

        registro = cursor_resultado.fetchone()

        if registro:
            return _convertir_resultados(
                cursor_resultado,
                [registro]
            )[0]

        return None

    except Exception:
        if conexion:
            conexion.rollback()
        raise

    finally:
        if cursor_resultado:
            cursor_resultado.close()

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()


def registrar_movimiento(
    id_producto,
    id_empleado,
    tipo_movimiento,
    cantidad,
    id_venta,
    observacion
):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_REGISTRAR_MOVIMIENTO_INVENTARIO",
            [
                id_producto,
                id_empleado,
                tipo_movimiento,
                cantidad,
                id_venta,
                observacion
            ]
        )

        conexion.commit()

    except Exception:
        if conexion:
            conexion.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if conexion:
            conexion.close()


def actualizar_movimiento(
    id_movimiento,
    tipo_movimiento,
    cantidad,
    id_empleado,
    id_venta,
    observacion
):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_MOVIMIENTO",
            [
                id_movimiento,
                tipo_movimiento,
                cantidad,
                id_empleado,
                id_venta,
                observacion
            ]
        )

        conexion.commit()

    except Exception:
        if conexion:
            conexion.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if conexion:
            conexion.close()


def eliminar_movimiento(id_movimiento):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_MOVIMIENTO",
            [id_movimiento]
        )

        conexion.commit()

    except Exception:
        if conexion:
            conexion.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if conexion:
            conexion.close()

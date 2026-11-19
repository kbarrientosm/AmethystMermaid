
import oracledb
from app.database.conexion import obtener_conexion


def listar_empleados():
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc("PR_LISTAR_EMPLEADOS", [resultado])

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        filas = cursor_resultado.fetchall()

        empleados = [
            dict(zip(columnas, fila))
            for fila in filas
        ]

        return empleados

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def buscar_empleado(id_empleado):
    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_EMPLEADO",
            [id_empleado, resultado]
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


def registrar_empleado(nombre, cargo, correo, contrasena, id_rol):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        id_empleado = cursor.var(oracledb.NUMBER)

        cursor.callproc(
            "PR_REGISTRAR_EMPLEADO",
            [
                nombre,
                cargo,
                correo,
                contrasena,
                id_rol,
                id_empleado
            ]
        )

        conexion.commit()

        return int(id_empleado.getvalue())

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def actualizar_empleado(
    id_empleado,
    nombre,
    cargo,
    correo,
    contrasena,
    id_rol
):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_EMPLEADO",
            [
                id_empleado,
                nombre,
                cargo,
                correo,
                contrasena,
                id_rol
            ]
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


def eliminar_empleado(id_empleado):
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_EMPLEADO",
            [id_empleado]
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


import oracledb

from app.database.conexion import obtener_conexion


def listar_productos():
    """
    Ejecuta PR_LISTAR_PRODUCTOS y devuelve todos los productos.
    """

    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_LISTAR_PRODUCTOS",
            [resultado]
        )

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        filas = cursor_resultado.fetchall()

        productos = [
            dict(zip(columnas, fila))
            for fila in filas
        ]

        return productos

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def buscar_producto(id_producto):
    """
    Ejecuta PR_BUSCAR_PRODUCTO y devuelve un producto por su ID.
    """

    conexion = None
    cursor = None
    cursor_resultado = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        resultado = cursor.var(oracledb.CURSOR)

        cursor.callproc(
            "PR_BUSCAR_PRODUCTO",
            [id_producto, resultado]
        )

        cursor_resultado = resultado.getvalue()

        columnas = [
            columna[0].lower()
            for columna in cursor_resultado.description
        ]

        fila = cursor_resultado.fetchone()

        if fila is None:
            return None

        producto = dict(zip(columnas, fila))

        return producto

    finally:
        if cursor_resultado is not None:
            cursor_resultado.close()

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def registrar_producto(
    nombre,
    descripcion,
    precio,
    stock,
    stock_minimo,
    id_categoria
):
    """
    Ejecuta PR_REGISTRAR_PRODUCTO y devuelve el ID generado.
    """

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        id_producto = cursor.var(oracledb.NUMBER)

        cursor.callproc(
            "PR_REGISTRAR_PRODUCTO",
            [
                nombre,
                descripcion,
                precio,
                stock,
                stock_minimo,
                id_categoria,
                id_producto
            ]
        )

        conexion.commit()

        return int(id_producto.getvalue())

    except Exception:
        if conexion is not None:
            conexion.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


def actualizar_producto(
    id_producto,
    nombre,
    descripcion,
    precio,
    stock_minimo,
    id_categoria
):
    """
    Ejecuta PR_ACTUALIZAR_PRODUCTO.
    No modifica las existencias actuales.
    """

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ACTUALIZAR_PRODUCTO",
            [
                id_producto,
                nombre,
                descripcion,
                precio,
                stock_minimo,
                id_categoria
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


def eliminar_producto(id_producto):
    """
    Ejecuta PR_ELIMINAR_PRODUCTO.
    """

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.callproc(
            "PR_ELIMINAR_PRODUCTO",
            [id_producto]
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


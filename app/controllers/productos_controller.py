
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database.productos_db import (
    listar_productos,
    buscar_producto,
    registrar_producto,
    actualizar_producto,
    eliminar_producto
)

from app.database.categorias_db import listar_categorias


productos_bp = Blueprint(
    "productos",
    __name__,
    url_prefix="/productos"
)


@productos_bp.route("/")
def listar():
    productos = listar_productos()
    return render_template("productos/listar.html", productos=productos)


@productos_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    categorias = listar_categorias()

    if request.method == "POST":
        try:
            nombre = request.form["nombre"]
            descripcion = request.form["descripcion"]
            precio = float(request.form["precio"])
            stock = int(request.form["stock"])
            stock_minimo = int(request.form["stock_minimo"])
            id_categoria = int(request.form["id_categoria"])

            registrar_producto(
                nombre,
                descripcion,
                precio,
                stock,
                stock_minimo,
                id_categoria
            )

            flash("Producto registrado correctamente.", "success")
            return redirect(url_for("productos.listar"))

        except Exception as error:
            flash(f"No se pudo registrar el producto: {error}", "error")

    return render_template(
        "productos/registrar.html",
        categorias=categorias
    )


@productos_bp.route("/editar/<int:id_producto>", methods=["GET", "POST"])
def editar(id_producto):
    producto = buscar_producto(id_producto)

    if producto is None:
        flash("El producto no existe.", "error")
        return redirect(url_for("productos.listar"))

    categorias = listar_categorias()

    if request.method == "POST":
        try:
            nombre = request.form["nombre"]
            descripcion = request.form["descripcion"]
            precio = float(request.form["precio"])
            stock_minimo = int(request.form["stock_minimo"])
            id_categoria = int(request.form["id_categoria"])

            actualizar_producto(
                id_producto,
                nombre,
                descripcion,
                precio,
                stock_minimo,
                id_categoria
            )

            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("productos.listar"))

        except Exception as error:
            flash(f"No se pudo actualizar el producto: {error}", "error")

    return render_template(
        "productos/editar.html",
        producto=producto,
        categorias=categorias
    )


@productos_bp.route("/eliminar/<int:id_producto>", methods=["POST"])
def eliminar(id_producto):
    try:
        eliminar_producto(id_producto)
        flash("Producto eliminado correctamente.", "success")

    except Exception as error:
        flash(f"No se pudo eliminar el producto: {error}", "error")

    return redirect(url_for("productos.listar"))


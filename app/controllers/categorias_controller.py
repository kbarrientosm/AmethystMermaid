
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database.categorias_db import (
    listar_categorias,
    buscar_categoria,
    registrar_categoria,
    actualizar_categoria,
    eliminar_categoria
)


categorias_bp = Blueprint(
    "categorias",
    __name__,
    url_prefix="/categorias"
)


@categorias_bp.route("/")
def listar():
    categorias = listar_categorias()
    return render_template(
        "categorias/listar.html",
        categorias=categorias
    )


@categorias_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        try:
            nombre = request.form["nombre"].strip()

            if not nombre:
                raise ValueError("El nombre de la categoría es obligatorio.")

            registrar_categoria(nombre)

            flash("Categoría registrada correctamente.", "success")
            return redirect(url_for("categorias.listar"))

        except Exception as error:
            flash(f"No se pudo registrar la categoría: {error}", "error")

    return render_template("categorias/registrar.html")


@categorias_bp.route("/editar/<int:id_categoria>", methods=["GET", "POST"])
def editar(id_categoria):
    categoria = buscar_categoria(id_categoria)

    if categoria is None:
        flash("La categoría no existe.", "error")
        return redirect(url_for("categorias.listar"))

    if request.method == "POST":
        try:
            nombre = request.form["nombre"].strip()

            if not nombre:
                raise ValueError("El nombre de la categoría es obligatorio.")

            actualizar_categoria(id_categoria, nombre)

            flash("Categoría actualizada correctamente.", "success")
            return redirect(url_for("categorias.listar"))

        except Exception as error:
            flash(f"No se pudo actualizar la categoría: {error}", "error")

    return render_template(
        "categorias/editar.html",
        categoria=categoria
    )


@categorias_bp.route("/eliminar/<int:id_categoria>", methods=["POST"])
def eliminar(id_categoria):
    try:
        eliminar_categoria(id_categoria)
        flash("Categoría eliminada correctamente.", "success")

    except Exception as error:
        flash(f"No se pudo eliminar la categoría: {error}", "error")

    return redirect(url_for("categorias.listar"))


from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database.clientes_db import (
    listar_clientes,
    buscar_cliente,
    registrar_cliente,
    actualizar_cliente,
    eliminar_cliente
)


clientes_bp = Blueprint(
    "clientes",
    __name__,
    url_prefix="/clientes"
)


@clientes_bp.route("/")
def listar():
    clientes = listar_clientes()

    return render_template(
        "clientes/listar.html",
        clientes=clientes
    )


@clientes_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        try:
            nombre = request.form["nombre"].strip()
            correo = request.form["correo"].strip()
            telefono = request.form["telefono"].strip()
            direccion = request.form["direccion"].strip()

            if not nombre or not correo or not telefono or not direccion:
                raise ValueError("Todos los campos son obligatorios.")

            registrar_cliente(
                nombre,
                correo,
                telefono,
                direccion
            )

            flash("Cliente registrado correctamente.", "success")

            return redirect(url_for("clientes.listar"))

        except Exception as error:
            flash(f"No se pudo registrar el cliente: {error}", "error")

    return render_template("clientes/registrar.html")


@clientes_bp.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar(id_cliente):
    cliente = buscar_cliente(id_cliente)

    if cliente is None:
        flash("El cliente no existe.", "error")
        return redirect(url_for("clientes.listar"))

    if request.method == "POST":
        try:
            nombre = request.form["nombre"].strip()
            correo = request.form["correo"].strip()
            telefono = request.form["telefono"].strip()
            direccion = request.form["direccion"].strip()

            if not nombre or not correo or not telefono or not direccion:
                raise ValueError("Todos los campos son obligatorios.")

            actualizar_cliente(
                id_cliente,
                nombre,
                correo,
                telefono,
                direccion
            )

            flash("Cliente actualizado correctamente.", "success")

            return redirect(url_for("clientes.listar"))

        except Exception as error:
            flash(f"No se pudo actualizar el cliente: {error}", "error")

    return render_template(
        "clientes/editar.html",
        cliente=cliente
    )


@clientes_bp.route("/eliminar/<int:id_cliente>", methods=["POST"])
def eliminar(id_cliente):
    try:
        eliminar_cliente(id_cliente)

        flash("Cliente eliminado correctamente.", "success")

    except Exception as error:
        flash(f"No se pudo eliminar el cliente: {error}", "error")

    return redirect(url_for("clientes.listar"))

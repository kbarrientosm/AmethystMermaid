
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database.roles_db import (
    listar_roles,
    buscar_rol,
    registrar_rol,
    actualizar_rol,
    eliminar_rol
)


roles_bp = Blueprint(
    "roles",
    __name__,
    url_prefix="/roles"
)


@roles_bp.route("/")
def listar():
    roles = listar_roles()

    return render_template(
        "roles/listar.html",
        roles=roles
    )


@roles_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre or not descripcion:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("roles.registrar"))

        try:
            registrar_rol(nombre, descripcion)

            flash("Rol registrado correctamente.", "success")

            return redirect(url_for("roles.listar"))

        except Exception as error:
            flash(f"No fue posible registrar el rol: {error}", "error")

    return render_template("roles/registrar.html")


@roles_bp.route("/editar/<int:id_rol>", methods=["GET", "POST"])
def editar(id_rol):
    rol = buscar_rol(id_rol)

    if rol is None:
        flash("El rol solicitado no existe.", "error")
        return redirect(url_for("roles.listar"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre or not descripcion:
            flash("Todos los campos son obligatorios.", "error")

            return render_template(
                "roles/editar.html",
                rol=rol
            )

        try:
            actualizar_rol(id_rol, nombre, descripcion)

            flash("Rol actualizado correctamente.", "success")

            return redirect(url_for("roles.listar"))

        except Exception as error:
            flash(f"No fue posible actualizar el rol: {error}", "error")

    return render_template(
        "roles/editar.html",
        rol=rol
    )


@roles_bp.route("/eliminar/<int:id_rol>", methods=["POST"])
def eliminar(id_rol):
    try:
        eliminar_rol(id_rol)

        flash("Rol eliminado correctamente.", "success")

    except Exception as error:
        flash(f"No fue posible eliminar el rol: {error}", "error")

    return redirect(url_for("roles.listar"))

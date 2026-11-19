
import re

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.database.empleados_db import (
    listar_empleados,
    buscar_empleado,
    registrar_empleado,
    actualizar_empleado,
    eliminar_empleado
)

from app.database.roles_db import listar_roles


empleados_bp = Blueprint(
    "empleados",
    __name__,
    url_prefix="/empleados"
)


def correo_valido(correo):
    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(patron, correo) is not None


@empleados_bp.route("/")
def listar():
    empleados = listar_empleados()

    return render_template(
        "empleados/listar.html",
        empleados=empleados
    )


@empleados_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    roles = listar_roles()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        cargo = request.form.get("cargo", "").strip()
        correo = request.form.get("correo", "").strip()
        contrasena = request.form.get("contrasena", "")
        id_rol = request.form.get("id_rol", "").strip()

        if not nombre or not cargo or not correo or not contrasena or not id_rol:
            flash("Todos los campos son obligatorios.", "error")

            return render_template(
                "empleados/registrar.html",
                roles=roles
            )

        if not correo_valido(correo):
            flash("Debe ingresar un correo electrónico válido.", "error")

            return render_template(
                "empleados/registrar.html",
                roles=roles
            )

        try:
            id_rol = int(id_rol)

            if not any(rol["id_rol"] == id_rol for rol in roles):
                flash("El rol seleccionado no es válido.", "error")

                return render_template(
                    "empleados/registrar.html",
                    roles=roles
                )

            registrar_empleado(
                nombre,
                cargo,
                correo,
                contrasena,
                id_rol
            )

            flash("Empleado registrado correctamente.", "success")

            return redirect(url_for("empleados.listar"))

        except ValueError:
            flash("El rol seleccionado no es válido.", "error")

        except Exception as error:
            flash(f"No fue posible registrar el empleado: {error}", "error")

    return render_template(
        "empleados/registrar.html",
        roles=roles
    )


@empleados_bp.route("/editar/<int:id_empleado>", methods=["GET", "POST"])
def editar(id_empleado):
    empleado = buscar_empleado(id_empleado)

    if empleado is None:
        flash("El empleado solicitado no existe.", "error")
        return redirect(url_for("empleados.listar"))

    roles = listar_roles()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        cargo = request.form.get("cargo", "").strip()
        correo = request.form.get("correo", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        id_rol = request.form.get("id_rol", "").strip()

        if not nombre or not cargo or not correo or not id_rol:
            flash("Debe completar todos los campos obligatorios.", "error")

            return render_template(
                "empleados/editar.html",
                empleado=empleado,
                roles=roles
            )

        if not correo_valido(correo):
            flash("Debe ingresar un correo electrónico válido.", "error")

            return render_template(
                "empleados/editar.html",
                empleado=empleado,
                roles=roles
            )

        try:
            id_rol = int(id_rol)

            if not any(rol["id_rol"] == id_rol for rol in roles):
                flash("El rol seleccionado no es válido.", "error")

                return render_template(
                    "empleados/editar.html",
                    empleado=empleado,
                    roles=roles
                )

            # Si el campo queda vacío, Oracle conserva la contraseña actual.
            if contrasena == "":
                contrasena = None

            actualizar_empleado(
                id_empleado,
                nombre,
                cargo,
                correo,
                contrasena,
                id_rol
            )

            flash("Empleado actualizado correctamente.", "success")

            return redirect(url_for("empleados.listar"))

        except ValueError:
            flash("El rol seleccionado no es válido.", "error")

        except Exception as error:
            flash(f"No fue posible actualizar el empleado: {error}", "error")

    return render_template(
        "empleados/editar.html",
        empleado=empleado,
        roles=roles
    )


@empleados_bp.route("/eliminar/<int:id_empleado>", methods=["POST"])
def eliminar(id_empleado):
    try:
        eliminar_empleado(id_empleado)

        flash("Empleado eliminado correctamente.", "success")

    except Exception as error:
        flash(f"No fue posible eliminar el empleado: {error}", "error")

    return redirect(url_for("empleados.listar"))

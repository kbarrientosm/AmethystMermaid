
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.database.ventas_db import (
    listar_ventas,
    buscar_venta,
    registrar_venta,
    actualizar_venta,
    eliminar_venta
)

from app.database.clientes_db import listar_clientes
from app.database.empleados_db import listar_empleados


ventas_bp = Blueprint(
    "ventas",
    __name__,
    url_prefix="/ventas"
)


ESTADOS_VALIDOS = [
    "Pendiente",
    "Completada",
    "Cancelada"
]


@ventas_bp.route("/")
def listar():
    ventas = listar_ventas()

    return render_template(
        "ventas/listar.html",
        ventas=ventas
    )


@ventas_bp.route("/ver/<int:id_venta>")
def ver(id_venta):
    venta = buscar_venta(id_venta)

    if venta is None:
        flash("La venta solicitada no existe.", "error")
        return redirect(url_for("ventas.listar"))

    return render_template(
        "ventas/ver.html",
        venta=venta
    )


@ventas_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    clientes = listar_clientes()
    empleados = listar_empleados()

    if request.method == "POST":
        metodo_pago = request.form.get(
            "metodo_pago", ""
        ).strip()

        estado = request.form.get(
            "estado", "Pendiente"
        ).strip()

        id_cliente = request.form.get(
            "id_cliente", ""
        ).strip()

        id_empleado = request.form.get(
            "id_empleado", ""
        ).strip()

        if not metodo_pago or not id_cliente or not id_empleado:
            flash("Debe completar todos los campos obligatorios.", "error")

            return render_template(
                "ventas/registrar.html",
                clientes=clientes,
                empleados=empleados,
                estados=ESTADOS_VALIDOS
            )

        try:
            id_cliente = int(id_cliente)
            id_empleado = int(id_empleado)

            if estado not in ESTADOS_VALIDOS:
                flash("El estado seleccionado no es vÃ¡lido.", "error")

                return render_template(
                    "ventas/registrar.html",
                    clientes=clientes,
                    empleados=empleados,
                    estados=ESTADOS_VALIDOS
                )

            if not any(
                cliente["id_cliente"] == id_cliente
                for cliente in clientes
            ):
                flash("El cliente seleccionado no es vÃ¡lido.", "error")

                return render_template(
                    "ventas/registrar.html",
                    clientes=clientes,
                    empleados=empleados,
                    estados=ESTADOS_VALIDOS
                )

            if not any(
                empleado["id_empleado"] == id_empleado
                for empleado in empleados
            ):
                flash("El empleado seleccionado no es vÃ¡lido.", "error")

                return render_template(
                    "ventas/registrar.html",
                    clientes=clientes,
                    empleados=empleados,
                    estados=ESTADOS_VALIDOS
                )

            id_nueva_venta = registrar_venta(
                metodo_pago,
                estado,
                id_cliente,
                id_empleado
            )

            flash(
                f"Venta registrada correctamente. NÃºmero de venta: {id_nueva_venta}.",
                "success"
            )

            return redirect(
                url_for(
                    "detalle_ventas.listar",
                    id_venta=id_nueva_venta
                )
            )

        except ValueError:
            flash("Los datos seleccionados no son vÃ¡lidos.", "error")

        except Exception as error:
            flash(f"No fue posible registrar la venta: {error}", "error")

    return render_template(
        "ventas/registrar.html",
        clientes=clientes,
        empleados=empleados,
        estados=ESTADOS_VALIDOS
    )


@ventas_bp.route("/editar/<int:id_venta>", methods=["GET", "POST"])
def editar(id_venta):
    venta = buscar_venta(id_venta)

    if venta is None:
        flash("La venta solicitada no existe.", "error")
        return redirect(url_for("ventas.listar"))

    if venta["estado"] != "Pendiente":
        flash(
            "Solo se pueden editar ventas pendientes.",
            "error"
        )
        return redirect(url_for("ventas.listar"))

    clientes = listar_clientes()
    empleados = listar_empleados()

    if request.method == "POST":
        metodo_pago = request.form.get(
            "metodo_pago", ""
        ).strip()

        estado = request.form.get(
            "estado", ""
        ).strip()

        id_cliente = request.form.get(
            "id_cliente", ""
        ).strip()

        id_empleado = request.form.get(
            "id_empleado", ""
        ).strip()

        if not metodo_pago or not id_cliente or not id_empleado:
            flash("Debe completar todos los campos obligatorios.", "error")

        else:
            try:
                id_cliente = int(id_cliente)
                id_empleado = int(id_empleado)

                if estado not in ESTADOS_VALIDOS:
                    flash("El estado seleccionado no es vÃ¡lido.", "error")

                elif not any(
                    cliente["id_cliente"] == id_cliente
                    for cliente in clientes
                ):
                    flash("El cliente seleccionado no es vÃ¡lido.", "error")

                elif not any(
                    empleado["id_empleado"] == id_empleado
                    for empleado in empleados
                ):
                    flash("El empleado seleccionado no es vÃ¡lido.", "error")

                else:
                    actualizar_venta(
                        id_venta,
                        metodo_pago,
                        estado,
                        id_cliente,
                        id_empleado
                    )

                    flash(
                        "Venta actualizada correctamente.",
                        "success"
                    )

                    return redirect(url_for("ventas.listar"))

            except ValueError:
                flash("Los datos seleccionados no son vÃ¡lidos.", "error")

            except Exception as error:
                flash(
                    f"No fue posible actualizar la venta: {error}",
                    "error"
                )

    return render_template(
        "ventas/editar.html",
        venta=venta,
        clientes=clientes,
        empleados=empleados,
        estados=ESTADOS_VALIDOS
    )


@ventas_bp.route("/eliminar/<int:id_venta>", methods=["POST"])
def eliminar(id_venta):
    try:
        venta = buscar_venta(id_venta)

        if venta is None:
            flash("La venta solicitada no existe.", "error")

        elif venta["id_venta"] == 1:
            flash(
                "La venta demostrativa no puede eliminarse.",
                "error"
            )

        else:
            eliminar_venta(id_venta)

            flash(
                "Venta eliminada correctamente.",
                "success"
            )

    except Exception as error:
        flash(
            f"No fue posible eliminar la venta: {error}",
            "error"
        )

    return redirect(url_for("ventas.listar"))


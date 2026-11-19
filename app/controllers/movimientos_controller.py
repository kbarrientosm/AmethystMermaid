
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database.movimientos_db import (
    listar_movimientos,
    buscar_movimiento,
    registrar_movimiento,
    actualizar_movimiento,
    eliminar_movimiento
)

from app.database.productos_db import listar_productos
from app.database.empleados_db import listar_empleados
from app.database.ventas_db import listar_ventas


movimientos_bp = Blueprint(
    "movimientos",
    __name__,
    url_prefix="/movimientos"
)


TIPOS_MOVIMIENTO = ["Entrada", "Salida", "Ajuste"]


@movimientos_bp.route("/")
def listar():
    movimientos = listar_movimientos()

    return render_template(
        "movimientos/listar.html",
        movimientos=movimientos
    )


@movimientos_bp.route("/registrar", methods=["GET", "POST"])
def registrar():

    productos = listar_productos()
    empleados = listar_empleados()
    ventas = listar_ventas()

    if request.method == "POST":

        try:
            id_producto = int(request.form["id_producto"])
            id_empleado = int(request.form["id_empleado"])

            tipo_movimiento = request.form["tipo_movimiento"]
            cantidad = int(request.form["cantidad"])

            id_venta = request.form.get("id_venta") or None

            if id_venta:
                id_venta = int(id_venta)

            observacion = request.form.get("observacion", "").strip()

            if tipo_movimiento not in TIPOS_MOVIMIENTO:
                raise ValueError("El tipo de movimiento seleccionado no es válido.")

            if cantidad == 0:
                raise ValueError("La cantidad debe ser diferente de cero.")

            if tipo_movimiento in ["Entrada", "Salida"] and cantidad < 0:
                raise ValueError("La cantidad de una entrada o salida debe ser positiva.")

            producto = next(
                (p for p in productos if p["id_producto"] == id_producto),
                None
            )

            if not producto:
                raise ValueError("El producto seleccionado no existe.")

            empleado = next(
                (e for e in empleados if e["id_empleado"] == id_empleado),
                None
            )

            if not empleado:
                raise ValueError("El empleado seleccionado no existe.")

            if id_venta is not None and not any(
                v["id_venta"] == id_venta for v in ventas
            ):
                raise ValueError("La venta seleccionada no existe.")

            registrar_movimiento(
                id_producto,
                id_empleado,
                tipo_movimiento,
                cantidad,
                id_venta,
                observacion
            )

            flash("Movimiento de inventario registrado correctamente.", "success")

            return redirect(url_for("movimientos.listar"))

        except (ValueError, KeyError) as error:
            flash(str(error), "error")

        except Exception as error:
            flash(f"No fue posible registrar el movimiento: {error}", "error")

    return render_template(
        "movimientos/registrar.html",
        productos=productos,
        empleados=empleados,
        ventas=ventas,
        tipos_movimiento=TIPOS_MOVIMIENTO
    )


@movimientos_bp.route("/editar/<int:id_movimiento>", methods=["GET", "POST"])
def editar(id_movimiento):

    movimiento = buscar_movimiento(id_movimiento)

    if not movimiento:
        flash("El movimiento solicitado no existe.", "error")
        return redirect(url_for("movimientos.listar"))

    if movimiento["tipo_movimiento"].strip().upper() == "AJUSTE":
        flash("Los movimientos de tipo Ajuste no pueden modificarse.", "error")
        return redirect(url_for("movimientos.listar"))

    productos = listar_productos()
    empleados = listar_empleados()
    ventas = listar_ventas()

    if request.method == "POST":

        try:
            tipo_movimiento = request.form["tipo_movimiento"]
            cantidad = int(request.form["cantidad"])
            id_empleado = int(request.form["id_empleado"])

            id_venta = request.form.get("id_venta") or None

            if id_venta:
                id_venta = int(id_venta)

            observacion = request.form.get("observacion", "").strip()

            if tipo_movimiento not in ["Entrada", "Salida"]:
                raise ValueError("El tipo de movimiento no es válido.")

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")

            if not any(
                e["id_empleado"] == id_empleado for e in empleados
            ):
                raise ValueError("El empleado seleccionado no existe.")

            if id_venta is not None and not any(
                v["id_venta"] == id_venta for v in ventas
            ):
                raise ValueError("La venta seleccionada no existe.")

            actualizar_movimiento(
                id_movimiento,
                tipo_movimiento,
                cantidad,
                id_empleado,
                id_venta,
                observacion
            )

            flash("Movimiento actualizado correctamente.", "success")

            return redirect(url_for("movimientos.listar"))

        except (ValueError, KeyError) as error:
            flash(str(error), "error")

        except Exception as error:
            flash(f"No fue posible actualizar el movimiento: {error}", "error")

    return render_template(
        "movimientos/editar.html",
        movimiento=movimiento,
        empleados=empleados,
        ventas=ventas
    )


@movimientos_bp.route("/eliminar/<int:id_movimiento>", methods=["POST"])
def eliminar(id_movimiento):

    movimiento = buscar_movimiento(id_movimiento)

    if not movimiento:
        flash("El movimiento solicitado no existe.", "error")
        return redirect(url_for("movimientos.listar"))

    if movimiento["tipo_movimiento"].strip().upper() == "AJUSTE":
        flash("Los movimientos de tipo Ajuste no pueden eliminarse.", "error")
        return redirect(url_for("movimientos.listar"))

    try:
        eliminar_movimiento(id_movimiento)

        flash("Movimiento eliminado correctamente.", "success")

    except Exception as error:
        flash(f"No fue posible eliminar el movimiento: {error}", "error")

    return redirect(url_for("movimientos.listar"))


from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database.facturas_db import (
    listar_facturas,
    buscar_factura,
    registrar_factura,
    actualizar_factura,
    eliminar_factura
)

from app.database.ventas_db import (
    listar_ventas,
    buscar_venta
)

from app.database.detalle_ventas_db import listar_detalles_venta


facturas_bp = Blueprint("facturas", __name__, url_prefix="/facturas")

IVA = 0.13


@facturas_bp.route("/")
def listar():
    facturas = listar_facturas()
    return render_template("facturas/listar.html", facturas=facturas)


@facturas_bp.route("/ver/<int:id_factura>")
def ver(id_factura):
    factura = buscar_factura(id_factura)

    if not factura:
        flash("La factura solicitada no existe.", "error")
        return redirect(url_for("facturas.listar"))

    return render_template("facturas/ver.html", factura=factura)


@facturas_bp.route("/registrar/<int:id_venta>", methods=["GET", "POST"])
def registrar(id_venta):
    venta = buscar_venta(id_venta)

    if not venta:
        flash("La venta seleccionada no existe.", "error")
        return redirect(url_for("ventas.listar"))

    facturas = listar_facturas()

    if any(factura["id_venta"] == id_venta for factura in facturas):
        flash("Esta venta ya tiene una factura registrada.", "error")
        return redirect(url_for("ventas.listar"))

    detalles = listar_detalles_venta(id_venta)

    if not detalles:
        flash("No se puede emitir una factura para una venta sin detalles.", "error")
        return redirect(url_for("ventas.listar"))

    subtotal = sum(detalle["subtotal"] for detalle in detalles)
    impuesto = round(subtotal * IVA, 2)

    if request.method == "POST":
        try:
            id_factura = registrar_factura(
                id_venta,
                subtotal,
                impuesto
            )

            flash("Factura registrada correctamente.", "success")
            return redirect(url_for("facturas.ver", id_factura=id_factura))

        except Exception as error:
            flash(f"No fue posible registrar la factura: {error}", "error")

    return render_template(
        "facturas/registrar.html",
        venta=venta,
        detalles=detalles,
        subtotal=subtotal,
        impuesto=impuesto,
        monto_total=subtotal + impuesto
    )


@facturas_bp.route("/editar/<int:id_factura>", methods=["GET", "POST"])
def editar(id_factura):
    factura = buscar_factura(id_factura)

    if not factura:
        flash("La factura solicitada no existe.", "error")
        return redirect(url_for("facturas.listar"))

    if id_factura == 1 or factura["id_venta"] == 1:
        flash("La factura demostrativa no puede modificarse.", "error")
        return redirect(url_for("facturas.listar"))

    venta = buscar_venta(factura["id_venta"])

    if not venta or venta["estado"] != "Pendiente":
        flash("Solo se pueden modificar facturas de ventas pendientes.", "error")
        return redirect(url_for("facturas.listar"))

    detalles = listar_detalles_venta(factura["id_venta"])

    if not detalles:
        flash("La venta no tiene detalles para calcular la factura.", "error")
        return redirect(url_for("facturas.listar"))

    subtotal = sum(detalle["subtotal"] for detalle in detalles)
    impuesto = round(subtotal * IVA, 2)

    if request.method == "POST":
        try:
            actualizar_factura(
                id_factura,
                subtotal,
                impuesto
            )

            flash("Factura actualizada correctamente.", "success")
            return redirect(url_for("facturas.ver", id_factura=id_factura))

        except Exception as error:
            flash(f"No fue posible actualizar la factura: {error}", "error")

    return render_template(
        "facturas/editar.html",
        factura=factura,
        venta=venta,
        detalles=detalles,
        subtotal=subtotal,
        impuesto=impuesto,
        monto_total=subtotal + impuesto
    )


@facturas_bp.route("/eliminar/<int:id_factura>", methods=["POST"])
def eliminar(id_factura):
    factura = buscar_factura(id_factura)

    if not factura:
        flash("La factura solicitada no existe.", "error")
        return redirect(url_for("facturas.listar"))

    if id_factura == 1 or factura["id_venta"] == 1:
        flash("La factura demostrativa no puede eliminarse.", "error")
        return redirect(url_for("facturas.listar"))

    try:
        eliminar_factura(id_factura)
        flash("Factura eliminada correctamente.", "success")

    except Exception as error:
        flash(f"No fue posible eliminar la factura: {error}", "error")

    return redirect(url_for("facturas.listar"))

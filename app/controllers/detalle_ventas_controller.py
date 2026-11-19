
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.database.detalle_ventas_db import (
    listar_detalles_venta,
    buscar_detalle_venta,
    registrar_detalle_venta,
    actualizar_detalle_venta,
    eliminar_detalle_venta
)

from app.database.ventas_db import (
    listar_ventas,
    buscar_venta
)

from app.database.productos_db import listar_productos


detalle_ventas_bp = Blueprint(
    "detalle_ventas",
    __name__,
    url_prefix="/detalle-ventas"
)


@detalle_ventas_bp.route("/venta/<int:id_venta>")
def listar(id_venta):
    venta = buscar_venta(id_venta)

    if venta is None:
        flash("La venta solicitada no existe.", "error")
        return redirect(url_for("ventas.listar"))

    detalles = listar_detalles_venta(id_venta)

    return render_template(
        "detalle_ventas/listar.html",
        detalles=detalles,
        venta=venta
    )


@detalle_ventas_bp.route("/registrar/<int:id_venta>", methods=["GET", "POST"])
def registrar(id_venta):
    venta = buscar_venta(id_venta)

    if venta is None:
        flash("La venta solicitada no existe.", "error")
        return redirect(url_for("ventas.listar"))

    if venta["estado"] != "Pendiente":
        flash(
            "Solo se pueden agregar productos a ventas pendientes.",
            "error"
        )
        return redirect(
            url_for("detalle_ventas.listar", id_venta=id_venta)
        )

    productos = listar_productos()

    if request.method == "POST":
        id_producto = request.form.get("id_producto", "").strip()
        cantidad = request.form.get("cantidad", "").strip()

        if not id_producto or not cantidad:
            flash("Debe completar todos los campos.", "error")

        else:
            try:
                id_producto = int(id_producto)
                cantidad = int(cantidad)

                if cantidad <= 0:
                    flash("La cantidad debe ser mayor que cero.", "error")

                else:
                    producto = next(
                        (
                            p for p in productos
                            if p["id_producto"] == id_producto
                        ),
                        None
                    )

                    if producto is None:
                        flash("El producto seleccionado no existe.", "error")

                    elif producto["stock"] < cantidad:
                        flash(
                            "La cantidad solicitada supera las existencias disponibles.",
                            "error"
                        )

                    else:
                        registrar_detalle_venta(
                            id_venta,
                            id_producto,
                            cantidad,
                            producto["precio"]
                        )

                        flash(
                            "Producto agregado a la venta correctamente.",
                            "success"
                        )

                        return redirect(
                            url_for(
                                "detalle_ventas.listar",
                                id_venta=id_venta
                            )
                        )

            except ValueError:
                flash("La cantidad o el producto no son válidos.", "error")

            except Exception as error:
                flash(
                    f"No fue posible agregar el producto: {error}",
                    "error"
                )

    return render_template(
        "detalle_ventas/registrar.html",
        venta=venta,
        productos=productos
    )


@detalle_ventas_bp.route(
    "/editar/<int:id_detalle>",
    methods=["GET", "POST"]
)
def editar(id_detalle):
    detalle = buscar_detalle_venta(id_detalle)

    if detalle is None:
        flash("El detalle solicitado no existe.", "error")
        return redirect(url_for("ventas.listar"))

    venta = buscar_venta(detalle["id_venta"])

    if venta is None or venta["estado"] != "Pendiente":
        flash(
            "Solo se pueden modificar detalles de ventas pendientes.",
            "error"
        )
        return redirect(
            url_for(
                "detalle_ventas.listar",
                id_venta=detalle["id_venta"]
            )
        )

    productos = listar_productos()

    if request.method == "POST":
        id_producto = request.form.get("id_producto", "").strip()
        cantidad = request.form.get("cantidad", "").strip()

        if not id_producto or not cantidad:
            flash("Debe completar todos los campos.", "error")

        else:
            try:
                id_producto = int(id_producto)
                cantidad = int(cantidad)

                if cantidad <= 0:
                    flash("La cantidad debe ser mayor que cero.", "error")

                else:
                    producto = next(
                        (
                            p for p in productos
                            if p["id_producto"] == id_producto
                        ),
                        None
                    )

                    if producto is None:
                        flash("El producto seleccionado no existe.", "error")

                    elif producto["stock"] < cantidad:
                        flash(
                            "La cantidad solicitada supera las existencias disponibles.",
                            "error"
                        )

                    else:
                        actualizar_detalle_venta(
                            id_detalle,
                            id_producto,
                            cantidad,
                            producto["precio"]
                        )

                        flash(
                            "Detalle actualizado correctamente.",
                            "success"
                        )

                        return redirect(
                            url_for(
                                "detalle_ventas.listar",
                                id_venta=detalle["id_venta"]
                            )
                        )

            except ValueError:
                flash("Los datos ingresados no son válidos.", "error")

            except Exception as error:
                flash(
                    f"No fue posible actualizar el detalle: {error}",
                    "error"
                )

    return render_template(
        "detalle_ventas/editar.html",
        detalle=detalle,
        venta=venta,
        productos=productos
    )


@detalle_ventas_bp.route(
    "/eliminar/<int:id_detalle>",
    methods=["POST"]
)
def eliminar(id_detalle):
    try:
        detalle = buscar_detalle_venta(id_detalle)

        if detalle is None:
            flash("El detalle solicitado no existe.", "error")
            return redirect(url_for("ventas.listar"))

        venta = buscar_venta(detalle["id_venta"])

        if venta is None or venta["estado"] != "Pendiente":
            flash(
                "Solo se pueden eliminar detalles de ventas pendientes.",
                "error"
            )

        else:
            eliminar_detalle_venta(id_detalle)

            flash(
                "Detalle eliminado correctamente.",
                "success"
            )

        return redirect(
            url_for(
                "detalle_ventas.listar",
                id_venta=detalle["id_venta"]
            )
        )

    except Exception as error:
        flash(
            f"No fue posible eliminar el detalle: {error}",
            "error"
        )

        return redirect(url_for("ventas.listar"))


import config

from flask import Flask, render_template

from app.database.productos_db import listar_productos

from app.controllers.productos_controller import productos_bp
from app.controllers.categorias_controller import categorias_bp
from app.controllers.clientes_controller import clientes_bp
from app.controllers.roles_controller import roles_bp
from app.controllers.empleados_controller import empleados_bp

from app.controllers.ventas_controller import ventas_bp
from app.controllers.detalle_ventas_controller import detalle_ventas_bp
from app.controllers.facturas_controller import facturas_bp
from app.controllers.movimientos_controller import movimientos_bp


def crear_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = config.SECRET_KEY

    app.register_blueprint(productos_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(empleados_bp)

    app.register_blueprint(ventas_bp)
    app.register_blueprint(detalle_ventas_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(movimientos_bp)

    @app.route("/")
    def inicio():

        productos = listar_productos()

        return render_template(
            "index.html",
            productos=productos
        )

    return app









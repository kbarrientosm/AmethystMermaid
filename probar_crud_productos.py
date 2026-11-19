
from app.database.productos_db import (
    listar_productos,
    buscar_producto,
    registrar_producto,
    actualizar_producto,
    eliminar_producto
)


print("===== PRUEBA CRUD PRODUCTOS =====")


# 1. LISTAR PRODUCTOS

print("\n--- 1. LISTAR PRODUCTOS ---")

productos = listar_productos()

for producto in productos:
    print(
        f"{producto['id_producto']} | "
        f"{producto['nombre']} | "
        f"{producto['categoria']} | "
        f"{producto['precio']} | "
        f"{producto['stock']}"
    )


# 2. REGISTRAR PRODUCTO

print("\n--- 2. REGISTRAR PRODUCTO ---")

id_nuevo = registrar_producto(
    "Producto de prueba",
    "Producto temporal para comprobar la integracion",
    5000,
    10,
    3,
    1
)

print("Producto registrado. ID:", id_nuevo)


# 3. BUSCAR PRODUCTO

print("\n--- 3. BUSCAR PRODUCTO ---")

producto = buscar_producto(id_nuevo)

if producto:
    print("ID:", producto["id_producto"])
    print("Nombre:", producto["nombre"])
    print("Categoria:", producto["categoria"])
    print("Precio:", producto["precio"])
    print("Stock:", producto["stock"])


# 4. ACTUALIZAR PRODUCTO

print("\n--- 4. ACTUALIZAR PRODUCTO ---")

actualizar_producto(
    id_nuevo,
    "Producto de prueba actualizado",
    "Descripcion actualizada",
    6000,
    4,
    1
)

producto = buscar_producto(id_nuevo)

print("Nombre actualizado:", producto["nombre"])
print("Precio actualizado:", producto["precio"])
print("Stock minimo actualizado:", producto["stock_minimo"])
print("Stock conservado:", producto["stock"])


# 5. ELIMINAR PRODUCTO

print("\n--- 5. ELIMINAR PRODUCTO ---")

eliminar_producto(id_nuevo)

producto = buscar_producto(id_nuevo)

if producto is None:
    print("Producto eliminado correctamente.")


print("\n===== FIN DE LA PRUEBA =====")

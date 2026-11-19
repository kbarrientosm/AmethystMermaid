
from app.database.conexion import obtener_conexion


try:
    conexion = obtener_conexion()

    print("¡Conexión exitosa con Oracle!")
    print("AmethystMermaid está conectada a ORCLPDB.")

    conexion.close()

    print("Conexión cerrada correctamente.")

except Exception as error:
    print("Error al conectar con Oracle:")
    print(error)

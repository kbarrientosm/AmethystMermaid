
import oracledb
import config


def obtener_conexion():
    """
    Establece una conexión con Oracle Database.
    """

    conexion = oracledb.connect(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        service_name=config.DB_SERVICE
    )

    return conexion

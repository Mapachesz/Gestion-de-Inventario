from config.db_config import get_connection
from models.product_model import Producto
from models.movimientos_model import Movimientos
from models.sub_compra_model import Sub_compra
from models.clientes_model import Clientes
from datetime import date
from typing import List

def agregar_cliente(cliente: Clientes) -> dict | None:
    """
    Inserta un nuevo cliente en la tabla 'clientes'.

    Parámetros:
        cliente (Clientes): Modelo validado con los datos del cliente.

    Retorna:
        dict | None: Cliente insertado o None si ocurre un error.
    """
    query = """
        INSERT INTO clientes (rut, nombre, direccion, celular, correo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """

    values = (
        cliente.rut,
        cliente.nombre,
        cliente.direccion,
        cliente.celular,
        cliente.correo
    )

    conn = get_connection()
    if not conn:
        return None

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                resultado = cursor.fetchone()
                columnas = [desc[0] for desc in cursor.description]
                return dict(zip(columnas, resultado))
    except Exception as e:
        print(f"❌ Error al agregar cliente: {e}")
        return None
    finally:
        conn.close()
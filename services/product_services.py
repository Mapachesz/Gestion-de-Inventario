from config.db_config import get_connection
from models.product_model import Producto
from datetime import date

def agregar_producto(producto: Producto):
    """
    Inserta un nuevo producto en la tabla 'productos'.

    Parámetros:
        producto (Producto): Modelo validado con los datos del producto.

    Retorna:
        dict | None: Producto insertado o None si ocurre un error.
    """
    query = """
        INSERT INTO productos (codigo, nombre, descripcion, stock, precio_unitario, fecha_ingreso)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
    """

    values = (
        producto.codigo,
        producto.nombre,
        producto.descripcion,
        producto.stock,
        producto.precio_unitario,
        producto.fecha_ingreso or date.today()
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
        print(f"❌ Error al agregar producto: {e}")
        return None
    finally:
        conn.close()

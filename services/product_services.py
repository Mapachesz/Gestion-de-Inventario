from config.db_config import get_connection
from models.product_model import Producto
from models.movimientos_model import Movimientos
from models.sub_compra_model import Sub_compra
from models.clientes_model import Clientes
from datetime import date
from typing import List

conn = get_connection()

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
        print(f"Error al agregar producto: {e}")
        return None
    finally:
        conn.close()

def editar_producto(producto: Producto):
    """
    Actualiza los datos de un producto existente, identificado por su código.

    Parámetros:
        producto (Producto): Modelo con los datos actualizados.

    Retorna:
        dict | None: Producto actualizado o None si no se encuentra o hay error.
    """
    query = """
        UPDATE productos
        SET nombre = %s,
            descripcion = %s,
            stock = %s,
            precio_unitario = %s,
            fecha_ingreso = %s
        WHERE codigo = %s
        RETURNING *;
    """

    values = (
        producto.nombre,
        producto.descripcion,
        producto.stock,
        producto.precio_unitario,
        producto.fecha_ingreso or date.today(),
        producto.codigo  # este va al final para el WHERE
    )

    if not conn:
        return None

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                resultado = cursor.fetchone()
                if resultado:
                    columnas = [desc[0] for desc in cursor.description]
                    return dict(zip(columnas, resultado))
                else:
                    print("Producto no encontrado para edición.")
                    return None
    except Exception as e:
        print(f"Error al editar producto: {e}")
        return None
    finally:
        conn.close()

def traer_productos() -> list[dict]:
    """
    Obtiene todos los productos almacenados en la base de datos.

    Retorna:
        list[dict]: Lista de productos (cada uno como diccionario).
    """
    query = "SELECT * FROM productos ORDER BY nombre ASC;"

    if not conn:
        return []

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()
                columnas = [desc[0] for desc in cursor.description]
                return [dict(zip(columnas, fila)) for fila in resultados]
    except Exception as e:
        print(f"Error al listar productos: {e}")
        return []
    finally:
        conn.close()

def eliminar_producto(codigo: str) -> bool:
    """
    Elimina un producto de la base de datos según su código.

    Parámetros:
        codigo (str): Código del producto a eliminar.

    Retorna:
        bool: True si se eliminó, False si no se encontró o falló.
    """
    query = "DELETE FROM productos WHERE codigo = %s RETURNING codigo;"

    if not conn:
        return False

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (codigo,))
                resultado = cursor.fetchone()
                return resultado is not None
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        conn.close()
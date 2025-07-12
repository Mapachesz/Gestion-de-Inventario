from config.db_config import get_connection
from models.product_model import Producto
from models.movimientos_model import Movimientos
from models.sub_compra_model import Sub_compra
from models.clientes_model import Clientes
from datetime import date
from typing import List

def registrar_movimiento(tipo: str, productos: List[dict], cliente_rut: str = None) -> dict | None:
    """
    Registra un movimiento de tipo 'Entrada' o 'Salida' con productos.

    Args:
        tipo (str): 'entrada' o 'salida' (insensible a mayúsculas)
        productos (List[dict]): [{'codigo', 'cantidad', 'precio_unitario'}, ...]
        cliente_rut (str): requerido solo si tipo es 'salida'

    Returns:
        dict | None: Movimiento insertado, o None si hay error.
    """

    conn = get_connection()
    if not conn:
        return None

    try:
        with conn:
            with conn.cursor() as cursor:
               

                # 🔹 Validar tipo permitido
                if tipo not in ('ingreso', 'egreso'):
                    raise ValueError("Tipo debe ser 'ingreso' o 'egreso'.")

                # 🔹 Validar existencia de cliente si es salida
                if tipo == 'ingreso':
                    cursor.execute("SELECT 1 FROM clientes WHERE rut = %s", (cliente_rut,))
                    if cursor.fetchone() is None:
                        raise ValueError(f"Cliente con RUT {cliente_rut} no existe.")

                # 🔹 Calcular total
                total = sum(p['cantidad'] * p['precio_unitario'] for p in productos)

                # 🔹 Crear objeto del movimiento
                movimiento = Movimientos(
                    id=0,
                    tipo=tipo,
                    fecha=date.today(),
                    total=total,
                    cliente_rut=cliente_rut if tipo == 'ingreso' else None
                )

                # 🔹 Insertar en movimientos
                cursor.execute("""
                    INSERT INTO movimientos (tipo, fecha, total, cliente_rut)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                """, (movimiento.tipo, movimiento.fecha, movimiento.total, movimiento.cliente_rut))

                movimiento_resultado = cursor.fetchone()
                columnas = [desc[0] for desc in cursor.description]
                movimiento_dict = dict(zip(columnas, movimiento_resultado))
                movimiento_id = movimiento_dict['id']

                # 🔹 Procesar cada producto
                for p in productos:
                    codigo = p['codigo']
                    cantidad = p['cantidad']
                    precio_unitario = p['precio_unitario']
                    subtotal = cantidad * precio_unitario

                    # Verificar existencia del producto
                    cursor.execute("SELECT stock FROM productos WHERE codigo = %s", (codigo,))
                    row = cursor.fetchone()
                    if not row:
                        raise ValueError(f"Producto con código '{codigo}' no existe.")
                    stock_actual = row[0]

                    # Validar stock suficiente si es salida
                    if tipo == 'ingreso' and cantidad > stock_actual:
                        raise ValueError(f"Stock insuficiente para '{codigo}': disponible {stock_actual}, solicitado {cantidad}.")

                    sub = Sub_compra(
                        id=0,
                        producto_codigo=codigo,
                        movimiento_id=movimiento_id,
                        cantidad=cantidad,
                        subtotal=subtotal
                    )

                    # Insertar detalle en sub_compra
                    cursor.execute("""
                        INSERT INTO sub_compra (producto_codigo, movimiento_id, cantidad, subtotal)
                        VALUES (%s, %s, %s, %s)
                    """, (sub.producto_codigo, sub.movimiento_id, sub.cantidad, sub.subtotal))

                    # Actualizar stock
                    cursor.execute(f"""
                        UPDATE productos
                        SET stock = stock {'+' if tipo == 'egreso' else '-'} %s
                        WHERE codigo = %s
                    """, (cantidad, codigo))

                return movimiento_dict

    except Exception as e:
        print(f"❌ Error al registrar movimiento: {e}")
        return None

    finally:
        conn.close()
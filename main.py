from models.product_model import Producto
from models.movimientos_model import Movimientos
from models.sub_compra_model import Sub_compra
from models.clientes_model import Clientes
from services.product_services import agregar_producto, editar_producto
from services.registrar_movimiento_service import  registrar_movimiento
from services.cliente_service import agregar_cliente
from datetime import date 


def main():
    print("🚀 Corriendo pruebas de inventario...\n")

    # 1️⃣ Registrar cliente (obligatorio para ingreso)
    cliente = Clientes(
        rut='12345678-2',
        nombre='Lucas Bernardo',
        direccion='Av. Siempre Muerta 742',
        celular='987632321',
        correo='seba@example.com'
    )

    cliente_resultado = agregar_cliente(cliente)
    if cliente_resultado:
        print("✅ Cliente agregado:", cliente_resultado)
    else:
        print("ℹ️ El cliente ya podría existir o hubo un error.")

    # 2️⃣ Registrar producto (solo si no existe)
    producto = Producto(
        codigo='P003',
        nombre='Lápiz verde',
        descripcion='Lápiz tinta verde punta fina',
        stock=100,
        precio_unitario=500,
        fecha_ingreso=date.today()
    )

    producto_resultado = agregar_producto(producto)
    if producto_resultado:
        print("✅ Producto agregado:", producto_resultado)
    else:
        print("ℹ️ El producto ya podría existir o hubo un error.")

    # 3️⃣ Registrar INGRESO (venta a cliente)
    productos_ingreso = [
        {'codigo': 'P003', 'cantidad': 5, 'precio_unitario': 700},
    ]
    movimiento_ingreso = registrar_movimiento('ingreso', productos_ingreso, cliente_rut='12345678-2')
    if movimiento_ingreso:
        print("✅ Ingreso (venta) registrado:", movimiento_ingreso)
    else:
        print("❌ Error al registrar ingreso (venta).")

if __name__ == "__main__":
    main()
#def main():
#    print("Corriendo...")

#if __name__ == "__main__":
#    main()

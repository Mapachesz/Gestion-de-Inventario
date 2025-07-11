from config.db_config import conectar_db

class Producto:
    def __init__(self, nombre, codigo, stock, precio):
        self.nombre = nombre
        self.codigo = codigo
        self.stock = stock
        self.precio = precio

    def insertar(self):
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO productos (nombre, codigo, stock, precio)
            VALUES (%s, %s, %s, %s)
        """, (self.nombre, self.codigo, self.stock, self.precio))
        conn.commit()
        cur.close()
        conn.close()

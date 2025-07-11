# db_config.py

import psycopg2
from dotenv import load_dotenv
import os

# Cargar variables desde archivo .env
load_dotenv()

# Extraer variables de entorno
DB_CONFIG = {
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "host": os.getenv("host"),
    "port": os.getenv("port", 5432),  # Puerto por defecto PostgreSQL
    "dbname": os.getenv("dbname")
}

def get_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        print("✅ Conexión exitosa a la base de datos.")
        return connection
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT NOW();")
                print("🕒 Hora actual:", cursor.fetchone()[0])
        finally:
            conn.close()
            print("🔒 Conexión cerrada.")

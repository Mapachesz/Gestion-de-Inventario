import psycopg2

def conectar_db():
    return psycopg2.connect(
        host="TU_HOST.supabase.co",
        dbname="postgres",
        user="postgres",
        password="TU_CLAVE",
        port="5432"
    )

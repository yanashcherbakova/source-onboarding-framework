import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        dbname="source_db",
        user="yana",
        password="1147"
    )
    return conn
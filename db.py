import psycopg2
import psycopg2.extras

def get_db_connection():
    psycopg2.extras.register_uuid()
    conn = psycopg2.connect(
        host="localhost",
        user="foodish",
        password="",
        database="foodish"
    )
    return conn

db = get_db_connection()

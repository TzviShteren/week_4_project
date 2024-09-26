import psycopg2
from psycopg2 import pool, extensions

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname="wwii_missions",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)


def get_db_connection():
    if connection_pool:
        conn = connection_pool.getconn()
        return conn


def release_db_connection(conn):
    connection_pool.putconn(conn)

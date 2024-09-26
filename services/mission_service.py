from db import get_db_connection, release_db_connection
import psycopg2
from services.logger import log, log_error, log_query


def get_all_mission(data):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query = """select * from mission limit 20;"""  # I limit 20 Because there is too much running
        log_query(data, query)
        cur.execute(query)
        rows = cur.fetchall()
        return True, rows
    except psycopg2.Error as e:
        log_error(e)
        return False
    finally:
        if cur:
            cur.close()
        release_db_connection(conn)


def get_by_id_mission(data, id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query = """select * from mission where mission_id = %s;"""
        log_query(data, query)
        cur.execute(query, id)
        rows = cur.fetchall()
        return True, rows
    except psycopg2.Error as e:
        log_error(e)
        return False
    finally:
        if cur:
            cur.close()
        release_db_connection(conn)

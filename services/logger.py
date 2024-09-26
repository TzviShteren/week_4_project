import logging
import datetime


def log_error(data):
    logging.error(f'{datetime.datetime.now()}: {data}')


def log(data):
    logging.info(
        f'{datetime.datetime.now()}: Accessed by: IP - {data["ip"]}, Where - {data["endpoint"]}, How - {data["method"]}')


def log_query(data, query):
    logging.info(
        f'{datetime.datetime.now()}: Accessed by: IP - {data["ip"]}, Where - {data["endpoint"]}, How - {data["method"]}, With - {query}')

from flask import Flask, request
from services.logger import *
import logging
from db import connection_pool
from services.normal_service import normalize_db

app = Flask(__name__)

logging.basicConfig(filename='db_logs.log', level=logging.INFO)


@app.route('/', methods=['GET'])
def hello_world():
    request_info = {
        "ip": request.remote_addr,
        "endpoint": request.url,
        "method": request.method
    }
    log(request_info)
    return 'Hello World!'


@app.teardown_appcontext
def close_pool(exception=None):
    if connection_pool:
        connection_pool.closeall()


if __name__ == '__main__':
    normalize_db()
    app.run(debug=True)

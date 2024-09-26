from flask import Flask, request

from controllers.mission_controller import mission_bp
from controllers.normalize_controller import normalize_bp
from services.logger import *
import logging
from db import connection_pool
from services.normal_service import normalize_db

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

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


app.register_blueprint(mission_bp, url_prefix="/mission")
app.register_blueprint(normalize_bp, url_prefix="/normalize")


# @app.teardown_appcontext
# def close_pool(exception=None):
#     if connection_pool:
#         connection_pool.closeall()


if __name__ == '__main__':
    app.run(debug=True)

# normalize_db()

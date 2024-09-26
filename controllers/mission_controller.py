from flask import Blueprint, request, jsonify
from services.mission_service import *

mission_bp = Blueprint('mission', __name__)


@mission_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'msg': 'It works!'}), 200


@mission_bp.route('/', methods=['GET'])
def all_mission():
    request_info = {
        "ip": request.remote_addr,
        "endpoint": request.url,
        "method": request.method
    }
    result = get_all_mission(request_info)
    if result:
        return jsonify({"result": result}), 201
    else:
        return jsonify({"result": result}), 400


@mission_bp.route('/<id>', methods=['GET'])
def one_mission(id):
    request_info = {
        "ip": request.remote_addr,
        "endpoint": request.url,
        "method": request.method
    }
    result = get_by_id_mission(request_info, id)
    if result:
        return jsonify({"result": result}), 201
    else:
        return jsonify({"result": result}), 400

from flask import Blueprint, jsonify
from services.normal_service import normalize_db


normalize_bp = Blueprint('normalize', __name__)

@normalize_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'msg': 'It works!'})


@normalize_bp.route('/start', methods=['POST'])
def start_normalize():
    result = normalize_db()
    if result is True:
        return jsonify({"result": result}), 201
    else:
        return jsonify({"result": result}), 400
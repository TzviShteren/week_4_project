from flask import Blueprint, request, jsonify
from services.mission_service import *

mission_bp = Blueprint('mission', __name__)


@mission_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'msg': 'It works!'})

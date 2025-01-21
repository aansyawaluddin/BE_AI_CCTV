from flask import Blueprint, request, jsonify
from .config import Session
from .models import CameraConfiguration

camera_config_bp = Blueprint('camera_config', __name__)

# GET Camera Configuration by ID
@camera_config_bp.route('/camera_config/<int:camera_id>', methods=['GET'])
def get_camera_config_by_id(camera_id):
    session = Session()
    try:
        camera_config = session.query(CameraConfiguration).filter(CameraConfiguration.id == camera_id).first()

        if not camera_config:
            return jsonify({"error": "Camera configuration not found", "code": 404}), 404

        return jsonify({
            "id": camera_config.id,
            "username": camera_config.username,
            "password": camera_config.password,
            "ip": camera_config.ip,
            "line_point_left": camera_config.line_point_left,
            "line_point_right": camera_config.line_point_right
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# POST Create Camera Configuration
@camera_config_bp.route('/camera_config', methods=['POST'])
def create_camera_config():
    session = Session()
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON payload"}), 400

        username = data.get('username')
        password = data.get('password')
        ip = data.get('ip')
        line_point_left = data.get('line_point_left')
        line_point_right = data.get('line_point_right')

        if not username or not password or not ip or not line_point_left or not line_point_right:
            return jsonify({"error": "Missing required fields"}), 400

        camera_config = CameraConfiguration(
            username=username,
            password=password,
            ip=ip,
            line_point_left=line_point_left,
            line_point_right=line_point_right
        )

        session.add(camera_config)
        session.commit()

        return jsonify({
            "id": camera_config.id,
            "username": camera_config.username,
            "password": camera_config.password,
            "ip": camera_config.ip,
            "line_point_left": camera_config.line_point_left,
            "line_point_right": camera_config.line_point_right
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# PUT Update Camera Configuration
@camera_config_bp.route('/camera_config/<int:camera_id>', methods=['PUT'])
def update_camera_config(camera_id):
    session = Session()
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON payload"}), 400

        username = data.get('username')
        password = data.get('password')
        ip = data.get('ip')
        line_point_left = data.get('line_point_left')
        line_point_right = data.get('line_point_right')

        if not username or not password or not ip or not line_point_left or not line_point_right:
            return jsonify({"error": "Missing required fields"}), 400

        camera_config = session.query(CameraConfiguration).filter(CameraConfiguration.id == camera_id).first()

        if not camera_config:
            return jsonify({"error": "Camera configuration not found", "code": 404}), 404

        camera_config.username = username
        camera_config.password = password
        camera_config.ip = ip
        camera_config.line_point_left = line_point_left
        camera_config.line_point_right = line_point_right

        session.commit()

        return jsonify({
            "id": camera_config.id,
            "username": camera_config.username,
            "password": camera_config.password,
            "ip": camera_config.ip,
            "line_point_left": camera_config.line_point_left,
            "line_point_right": camera_config.line_point_right
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# DELETE Camera Configuration
@camera_config_bp.route('/camera_config/<int:camera_id>', methods=['DELETE'])
def delete_camera_config(camera_id):
    session = Session()
    try:
        camera_config = session.query(CameraConfiguration).filter(CameraConfiguration.id == camera_id).first()

        if not camera_config:
            return jsonify({"error": "Camera configuration not found", "code": 404}), 404

        session.delete(camera_config)
        session.commit()

        return jsonify({"message": "Camera configuration deleted successfully"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

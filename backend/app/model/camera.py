from flask import Blueprint, request, jsonify
from .config import Session
from .models import Camera, Location

camera_bp = Blueprint('camera', __name__)

# GET Camera by ID
@camera_bp.route('/camera/<int:camera_id>', methods=['GET'])
def get_camera(camera_id):
    session = Session()
    try:
        camera = session.query(Camera).filter_by(id=camera_id).first()

        if not camera:
            return jsonify({"error": "Camera not found"}), 404

        return jsonify({
            "id": camera.id,
            "name_camera": camera.name_camera,
            "type_camera": camera.type_camera,
            "status": camera.status,
            "ip_address": camera.ip_address,
            "location_id": camera.id_location
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# POST Camera
@camera_bp.route('/camera', methods=['POST'])
def create_camera():
    session = Session()
    try:
        data = request.get_json()

        name_camera = data.get('name_camera')
        type_camera = data.get('type_camera')
        ip_address = data.get('ip_address')
        status = data.get('status')
        location_id = data.get('id_location')

        if not name_camera or not type_camera or not ip_address:
            return jsonify({"error": "Missing required fields"}), 400

        camera = Camera(
            name_camera=name_camera,
            type_camera=type_camera,
            ip_address=ip_address,
            status=status,
            id_location=location_id
        )

        session.add(camera)
        session.commit()

        return jsonify({
            "id": camera.id,
            "name_camera": camera.name_camera,
            "type_camera": camera.type_camera,
            "status": camera.status,
            "ip_address": camera.ip_address,
            "location_id": camera.id_location
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# PUT Camera
@camera_bp.route('/camera/<int:camera_id>', methods=['PUT'])
def update_camera(camera_id):
    session = Session()
    try:
        data = request.get_json()

        name_camera = data.get('name_camera')
        type_camera = data.get('type_camera')
        ip_address = data.get('ip_address')
        status = data.get('status')
        location_id = data.get('id_location')

        if not name_camera or not type_camera or not ip_address:
            return jsonify({"error": "Missing required fields"}), 400

        camera = session.query(Camera).filter_by(id=camera_id).first()

        if not camera:
            return jsonify({"error": "Camera not found"}), 404

        camera.name_camera = name_camera
        camera.type_camera = type_camera
        camera.ip_address = ip_address
        camera.status = status
        camera.id_location = location_id

        session.commit()

        return jsonify({
            "id": camera.id,
            "name_camera": camera.name_camera,
            "type_camera": camera.type_camera,
            "status": camera.status,
            "ip_address": camera.ip_address,
            "location_id": camera.id_location
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# DELETE Camera
@camera_bp.route('/camera/<int:camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    session = Session()
    try:
        camera = session.query(Camera).filter_by(id=camera_id).first()

        if not camera:
            return jsonify({"error": "Camera not found"}), 404

        session.delete(camera)
        session.commit()

        return jsonify({"message": "Camera deleted successfully"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

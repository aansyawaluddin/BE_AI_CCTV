from flask import Blueprint, request, jsonify
from .config import Session
from .models import Recording, Camera

recording_bp = Blueprint('recording', __name__)

# GET Recording by ID
@recording_bp.route('/recording/<int:recording_id>', methods=['GET'])
def get_recording(recording_id):
    session = Session()
    try:
        recording = session.query(Recording).filter_by(id=recording_id).first()

        if not recording:
            return jsonify({"error": "Recording not found"}), 404

        return jsonify({
            "id": recording.id,
            "encode_type": recording.encode_type,
            "status": recording.status,
            "camera_id": recording.id_camera
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# POST Recording
@recording_bp.route('/recording', methods=['POST'])
def create_recording():
    session = Session()
    try:
        data = request.get_json()

        encode_type = data.get('encode_type')
        status = data.get('status')
        camera_id = data.get('id_camera')

        if not camera_id:
            return jsonify({"error": "Missing required fields"}), 400

        recording = Recording(
            encode_type=encode_type,
            status=status,
            id_camera=camera_id
        )

        session.add(recording)
        session.commit()

        return jsonify({
            "id": recording.id,
            "encode_type": recording.encode_type,
            "status": recording.status,
            "camera_id": recording.id_camera
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# PUT Recording
@recording_bp.route('/recording/<int:recording_id>', methods=['PUT'])
def update_recording(recording_id):
    session = Session()
    try:
        data = request.get_json()

        encode_type = data.get('encode_type')
        status = data.get('status')
        camera_id = data.get('id_camera')

        if not camera_id:
            return jsonify({"error": "Missing required fields"}), 400

        recording = session.query(Recording).filter_by(id=recording_id).first()

        if not recording:
            return jsonify({"error": "Recording not found"}), 404

        recording.encode_type = encode_type
        recording.status = status
        recording.id_camera = camera_id

        session.commit()

        return jsonify({
            "id": recording.id,
            "encode_type": recording.encode_type,
            "status": recording.status,
            "camera_id": recording.id_camera
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# DELETE Recording
@recording_bp.route('/recording/<int:recording_id>', methods=['DELETE'])
def delete_recording(recording_id):
    session = Session()
    try:
        recording = session.query(Recording).filter_by(id=recording_id).first()

        if not recording:
            return jsonify({"error": "Recording not found"}), 404

        session.delete(recording)
        session.commit()

        return jsonify({"message": "Recording deleted successfully"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

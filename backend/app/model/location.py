from flask import Blueprint, request, jsonify
from .config import Session
from .models import Location

location_bp = Blueprint('location', __name__)

# GET Location
@location_bp.route('/location/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id):
    session = Session()
    try:
        location = session.query(Location).filter_by(id=location_id).first()

        if not location:
            return jsonify({"error": "Location not found"}), 404

        return jsonify({
            "id": location.id,
            "name_location": location.name_location,
            "address_location": location.address_location
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST Location
@location_bp.route('/location', methods=['POST'])
def create_location():
    session = Session()
    try:
        data = request.get_json()

        name_location = data.get('name_location')
        address_location = data.get('address_location')

        if not name_location or not address_location:
            return jsonify({"error": "Missing required fields"}), 400

        location = Location(
            name_location=name_location,
            address_location=address_location
        )

        session.add(location)
        session.commit()

        return jsonify({
            "id": location.id,
            "name_location": location.name_location,
            "address_location": location.address_location
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# PUT Location
@location_bp.route('/location/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    session = Session()
    try:
        data = request.get_json()

        name_location = data.get('name_location')
        address_location = data.get('address_location')

        if not name_location or not address_location:
            return jsonify({"error": "Missing required fields"}), 400

        location = session.query(Location).filter_by(id=location_id).first()

        if not location:
            return jsonify({"error": "Location not found"}), 404

        location.name_location = name_location
        location.address_location = address_location

        session.commit()

        return jsonify({
            "id": location.id,
            "name_location": location.name_location,
            "address_location": location.address_location
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# DELETE Location
@location_bp.route('/location/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    session = Session()
    try:
        location = session.query(Location).filter_by(id=location_id).first()

        if not location:
            return jsonify({"error": "Location not found"}), 404

        session.delete(location)
        session.commit()

        return jsonify({"message": "Location deleted successfully"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

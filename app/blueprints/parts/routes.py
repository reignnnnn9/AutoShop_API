from app.blueprints.parts import part_bp
from .schemas import part_schema, parts_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Inventory, db, TicketInventory


@part_bp.route('', methods=['POST'])
def create_part():
    try:
        data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_part = Inventory(**data)
    db.session.add(new_part)
    db.session.commit()
    return part_schema.jsonify(new_part), 201

@part_bp.route('<int:inventory_id>', methods=['GET'])
def read_part(inventory_id):
    part = db.session.get(Inventory, inventory_id)
    print(part)
    return part_schema.jsonify(part), 200

@part_bp.route('<int:inventory_id>', methods=['PUT'])
def update_part(inventory_id):
    part = db.session.get(Inventory, inventory_id)

    if not part:
        return jsonify({"message": "part not found"}), 404
    
    try:
        part_data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in part_data.items():
        setattr(part, key, value)

    db.session.commit()
    return part_schema.jsonify(part), 200

@part_bp.route('<int:inventory_id>', methods=['DELETE'])
def delete_part(inventory_id):
    part = db.session.get(Inventory, inventory_id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted part#{inventory_id}"}), 200
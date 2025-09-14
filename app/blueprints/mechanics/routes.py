from app.blueprints.mechanics import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanics, db

@mechanic_bp.route('', methods=['POST'])
def create_mech():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanics(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanic_bp.route('', methods=['GET'])
def read_mechs():
    mechanics = db.session.query(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanic_bp.route('<int:mechanic_id>', methods=['GET'])
def read_a_mech(mechanic_id):
    mech  = db.session.get(Mechanics, mechanic_id)
    print(mech)
    return mechanic_schema.jsonify(mech), 200

@mechanic_bp.route('<int:mechanic_id>', methods=['PUT'])
def update_mech(mechanic_id):
    mech = db.session.get(Mechanics, mechanic_id)

    if not mech:
        return jsonify({"message": "Mechanic not found"}), 404
    
    try:
        mech_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"messages": e.messages}), 400
    
    for key, value in mech_data.items():
        setattr(mech, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mech), 200

@mechanic_bp.route('<int:mechanic_id>', methods=['DELETE'])
def delete_mech(mechanic_id):
    mech = db.session.get(Mechanics, mechanic_id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Succesfully deleted mechanic {mechanic_id}"}), 200
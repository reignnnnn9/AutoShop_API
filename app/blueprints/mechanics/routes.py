from app.blueprints.mechanics import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanics, db
from app.extensions import ma, limiter, cache
from sqlalchemy import select   

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
@cache.cached(timeout=60)
def read_mechs():
    # try:
    #     page = int(request.args.get('page'))
    #     per_page = int(request.args.get('per_page'))
    #     query = select(Mechanics)
    #     mechs = db.paginate(query, page=page, per_page=per_page) # Handles pagination
    #     return mechanics_schema.jsonify(mechs), 200

    # except: # Defaulting to regular if they don't send a page or page number
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

# Get popular Mechanics
@mechanic_bp.route('/popularity', methods=['GET'])
def get_popular_mechs():
    mechs = db.session.query(Mechanics).all() # Grabbing all mechanics from DB

    # Sort mechs list based off of how many service tickets they've been a part of
    mechs.sort(key= lambda mech: len(mech.service_tickets), reverse=True) # Reversing to get the most popular mechanics

    output = []
    for mech in mechs[:5]:
        mech_format = {
            "mech": mechanic_schema.dump(mech), # Translates the mech to json
            "serviced": len(mech.service_tickets) # Add the amount of serviced customers
        }
        output.append(mech_format) # Appends this dict to an output list

    return jsonify(output)


# Search for mechanic based on name or email
@mechanic_bp.route('/search', methods=['GET'])
def search_mech():
    name = request.args.get('name') # Accessing the query parameters from the URL
    email = request.args.get('email') # Accessing the query parameters from the URL

    if name:
        mechs = db.session.query(Mechanics).where(Mechanics.name.like(f'%{name}%')).all()
    elif email:
        mechs = db.session.query(Mechanics).where(Mechanics.email.like(f'%{email}%')).all()

    return mechanics_schema.jsonify(mechs), 200
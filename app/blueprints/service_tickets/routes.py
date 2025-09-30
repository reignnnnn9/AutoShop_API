from app.blueprints.service_tickets import ticket_bp
from .schemas import ticket_schema, tickets_schema
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTickets, Mechanics, db, TicketInventory
from app.extensions import cache

@ticket_bp.route('', methods=['POST'])
def create_ticket():
    try:
        data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = ServiceTickets(**data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

# PUT '/<ticket_id>/assign-mechanic/<mechanic-id>: 
# Adds a relationship between a service ticket and the mechanics. 
# (Reminder: use your relationship attributes! 
# They allow you the treat the relationship like a list, 
# able to append a Mechanic to the mechanics list).
@ticket_bp.route('<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mech(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({'message': "Service ticket not found"}), 404
  
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({'message': "Mechanic not found"}), 404
  
    if mechanic in ticket.mechanics:
        return jsonify({'message': 'Mechanic already assigned to ticket'}), 200
    else:
        ticket.mechanics.append(mechanic)
        db.session.commit()
        return jsonify({'message': f'Mechanic {mechanic_id} assigned to ticket {ticket_id}'}), 200

#PUT '/<ticket_id>/remove-mechanic/<mechanic-id>: 
# Removes the relationship from the service ticket and the mechanic.
@ticket_bp.route('<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mech(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({'message': "Service ticket not found"}), 404
  
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({'message': "Mechanic not found"}), 404
    
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
        return jsonify({'message': f'Mechanic {mechanic_id} removed from ticket {ticket_id}'}), 200
    else:
        return jsonify({'message': 'Mechanic provided is not assigned to ticket'}), 200


@ticket_bp.route('', methods=['GET'])
@cache.cached(timeout=60)
def read_tickets():
    tickets = db.session.query(ServiceTickets).all()
    return tickets_schema.jsonify(tickets), 200

@ticket_bp.route('<int:service_tickets_id>/add-item/<int:inventory_id>/<int:qty>', methods=['PUT'])
def add_part_to_ticket(service_tickets_id, inventory_id, qty):
    new_ticket_part = TicketInventory(inv_id=inventory_id, ticket_id=service_tickets_id, quantity=qty)
    db.session.add(new_ticket_part)
    db.session.commit()
    return jsonify({"message": "Successfully added part to service ticket"})
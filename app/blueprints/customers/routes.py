from app.blueprints.customers import customer_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db

# Create new customer
# Create route
@customer_bp.route('', methods=['POST']) # Route serves as trigger for below function
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 # Returns error as response
    
    new_customer = Customers(**data) # Creating Customer object
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# Read/View all customers
@customer_bp.route('', methods=['GET'])
def read_customers():
    customers = db.session.query(Customers).all()
    return customers_schema.jsonify(customers), 200

# Read/View one customer by id - Using a Dynamic Endpoint
@customer_bp.route('<int:customer_id>', methods=['GET'])
def read_cust(customer_id):
    cust = db.session.get(Customers, customer_id)
    print(cust)
    return customer_schema.jsonify(cust), 200

# Delete customer
@customer_bp.route('<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer {customer_id}"}), 200

# Update customer
@customer_bp.route('<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id) # Query for who to update

    if not customer: # Checking if we get customer
        return jsonify({"message": "customer not found"}), 404
    
    try:
        cust_data = customer_schema.load(request.json) # Validating updates
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in cust_data.items(): # Loop over attributes and values from cust data dict
        setattr(customer, key, value) # Setting (object, attribute, value) to replace

    db.session.commit()
    return customer_schema.jsonify(customer), 200
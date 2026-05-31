from .schemas import customer_schema, customers_schema, login_schema
from app.blueprints.service_ticket.schemas import service_tickets_schema 
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db, Service_Ticket
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required


@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)

        response = {
            'status': 'success',
            'message': 'successfully logged in',
            'token': token
        }

        return jsonify(response), 200
    
    else:
        return jsonify({'message': 'Invalid email or password'}), 400


# Create customer (POST) - C in CRUD
@customers_bp.route('/', methods=['POST'])
# limit request to 5 customers per day (per ip address)
# do not want too many customers to overwhelm sysyem
@limiter.limit("5 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({'error': 'Email already associated with an account'}), 400

    new_customer = Customer(**customer_data)

    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


# Get all Customers (GET) - R in CRUD
@customers_bp.route('/', methods=['GET'])
# Caching all members wil help speed up searches
#@cache.cached(timeout=60)  # 60 seconds
def get_customers():

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))

        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)

        return customers_schema.jsonify(customers), 200
    
    except:
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()

        return customers_schema.jsonify(customers)


# Get Specific Customer (GET) - R in CRUD
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    
    return jsonify({'error': 'Customer not found.'}), 404


# Get Service_Ticket related to a specific customer - R in CRUD
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
# limit request to 5 times per day
# limit edit requests to preserve integrity of customer data
@limiter.limit("5 per day")
def get_customer_ticket(customer_id):

    query = select(Service_Ticket).where(Service_Ticket.customer_id == customer_id)
    customer_tickets = db.session.execute(query).scalars().all()


    return service_tickets_schema.jsonify(customer_tickets), 200
        

# Update Specific Customer (PUT) - U in CRUD
@customers_bp.route('/', methods=['PUT'])
@token_required
# limit request to 5 times per day
# limit edit requests to preserve integrity of customer data
@limiter.limit("5 per day")
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({'error': 'Customer not found.'}), 404
    
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


# Delete Specific Customer (DELETE) - D in CRUD
@customers_bp.route('/', methods=['DELETE'])
@token_required
# limit request to 5 times per day
# want to limit customer account deletion to preserve customer data for company / legal reasons
@limiter.limit("5 per day")
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({'error': 'Customer not found.'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer id: {customer_id}, sucessfully deleted.'}), 200



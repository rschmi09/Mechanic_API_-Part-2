from .schemas import service_ticket_schema, service_tickets_schema, edit_service_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Service_Ticket, db, Inventory
from . import service_tickets_bp
from app.models import Mechanic


# Create Service Ticket (POST) - C in CRUD
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_Ticket(**service_ticket_data)

    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201


# Get all Service Tickets (GET) - R in CRUD
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))

        query = select(Service_Ticket)
        service_tickets = db.paginate(query, page=page, per_page=per_page)

        return service_tickets_schema.jsonify(service_tickets), 200        

    except:
        query = select(Service_Ticket)
        service_tickets = db.session.execute(query).scalars().all()

        return service_tickets_schema.jsonify(service_tickets)


# Get Specific Service_Ticket (GET) - R in CRUD
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)

    if service_ticket:
        return service_ticket_schema.jsonify(service_ticket), 200
    return jsonify({'error': 'Service_Ticket not found.'}), 404


# Update Specific Service_Ticket (PUT) - U in CRUD
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)

    if not service_ticket:
        return jsonify({'error': 'Service_Ticket not found.'}), 404
    
    try:
        service_ticket_data = service_ticket_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in service_ticket_data.items():
        setattr(service_ticket, key, value)

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


# Assign Mechanic (PUT) - U in CRUD
@service_tickets_bp.route('/<int:service_ticket_id>/edit', methods=['PUT'])
#def assign_mechanic(service_ticket_id, mechanic_id):
    #service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    #mechanic = db.session.get(Mechanic, mechanic_id)

    #if not service_ticket:
        #return jsonify({'error': 'Service ticket not found.'}), 404
    
    #if not mechanic:
        #return jsonify({'error': 'Mechanic not found.'})
    
    #service_ticket.mechanics.append(mechanic)

    #db.session.commit()
    #return jsonify({'messaege': f'Mechanic {mechanic_id} assigned to service ticket {service_ticket_id}'}), 200

def assign_mechanic(service_ticket_id):
    try:
        ticket_edits = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Service_Ticket).where(Service_Ticket.id == service_ticket_id)
    mechanic = db.session.execute(query).scalars().first()


    # Add mechanics
    for mechanic_id in ticket_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        new_mechanic = db.session.execute(query).scalars().first()

        if new_mechanic and new_mechanic not in mechanic.mechanics:
            mechanic.mechanics.append(new_mechanic)


    # Remove mechanics
    for mechanic_id in ticket_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        new_mechanic = db.session.execute(query).scalars().first()

        if new_mechanic and new_mechanic in mechanic.mechanics:
            mechanic.mechanics.remove(new_mechanic)

    db.session.commit()

    return service_ticket_schema.jsonify(mechanic), 200


# Remove Mechanic (PUT) - U in CRUD
#@service_tickets_bp.route('/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
#def remove_mechanic(service_ticket_id, mechanic_id):
    #service_ticket = db.session.get(Service_Ticket, service_ticket_id)
   #mechanic = db.session.get(Mechanic, mechanic_id)

    #if not service_ticket:
        #return jsonify({'error': "Service ticket not found."}), 404
    
    #if not mechanic:
        #return jsonify({'error': 'Mechanic not found.'}), 404
    
    #if mechanic not in service_ticket.mechanics:
        #return jsonify({'error': 'Mechanic not assigned to this ticket.'}), 400
    
    #service_ticket.mechanics.remove(mechanic)

    #db.session.commit()
    #return jsonify({'message': f'Mechanic {mechanic_id} removed from service ticket {service_ticket_id}.'}), 200


# Add a Single Inventory Item to an existing Service Ticket - U in CRUD
@service_tickets_bp.route('/<int:service_ticket_id>/edit/<int:inventory_id>', methods=['PUT'])
def add_item(service_ticket_id, inventory_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)
    inventory = db.session.get(Inventory, inventory_id)

    if not service_ticket:
        return jsonify({'error': 'Service Ticket not found.'}), 404
    
    if not inventory:
        return jsonify({'error': 'Item not found.'}), 404
    
    service_ticket.inventories.append(inventory)

    db.session.commit()
    return jsonify({'message': f'Item {inventory_id} has been added to Service Ticket {service_ticket_id}'}), 200

#---------------------------
# Add and Remove an Inventory Item - U in CRUD








# Delete Specific Service_Ticket (DELETE) - D in CRUD
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Ticket, service_ticket_id)

    if not service_ticket:
        return jsonify({'error': 'Service_Ticket not found.'}), 404
    
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({'message': f'Service_Ticket id: {service_ticket_id}, sucessfully deleted.'}), 200
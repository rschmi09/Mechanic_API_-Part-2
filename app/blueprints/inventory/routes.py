from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select 
from app.models import Inventory, db
from . import inventories_bp
from app.models import Service_Ticket


# Create Inventory Item (POST) - C in CRUD
@inventories_bp.route('/', methods=['POST'])
def create_inventory_item():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_item = Inventory(**inventory_data)

    db.session.add(new_item)
    db.session.commit()
    return inventory_schema.jsonify(new_item), 201


# Get All Inventory Items (GET) - R in CRUD
@inventories_bp.route('/', methods=['GET'])
def get_inventory_items():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))

        query = select(Inventory)
        inventory = db.paginate(query, page=page, per_page=per_page)

        return inventories_schema.jsonify(inventory), 200
    
    except:
        query = select(Inventory)
        inventory = db.session.execute(query).scalars().all()

        return inventories_schema.jsonify(inventory), 200


# Get Specific Inventory Item (GET) - R in CRUD
@inventories_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)

    if item:
        return inventory_schema.jsonify(item), 200
    return jsonify({'error': 'Item not found.'}), 404


# Update Specific Inventory Item (PUT) - U in CRUD
@inventories_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_item(inventory_id):
    update_item = db.session.get(Inventory, inventory_id)

    if not update_item:
        return jsonify({'error': 'Item not found.'}), 404
    
    try:
        item_data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in item_data.items():
        setattr(update_item, key, value)

    db.session.commit()
    return inventory_schema.jsonify(update_item), 200


# Delte Specific Inventory Item - D in CRUD
@inventories_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Item id: {inventory_id}, sucessfully deleted.'}), 200

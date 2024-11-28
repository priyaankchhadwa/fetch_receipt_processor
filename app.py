from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from uuid import uuid4
from datetime import datetime
import json
from datetime import datetime, date, time

from models import Receipt, Item
from points_calculator import calculate_points

app = Flask(__name__)

# In-memory storage for receipts and points
receipt_store = {}
receipt_points_store = {}

def parse_receipt(data):
    """Parse and validate receipt data"""
    try:
        # Parse dates and times
        purchase_date = datetime.strptime(data['purchaseDate'], '%Y-%m-%d').date()
        purchase_time = datetime.strptime(data['purchaseTime'], '%H:%M').time()

        # Convert items
        items = [
            Item(
                short_description=item['shortDescription'], 
                price=float(item['price'])
            ) for item in data['items']
        ]

        return Receipt(
            retailer=data['retailer'],
            purchase_date=purchase_date,
            purchase_time=purchase_time,
            items=items,
            total=float(data['total'])
        )
    except (KeyError, ValueError) as e:
        raise BadRequest("The receipt is invalid")

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    # Get JSON data
    data = request.get_json()
    
    # Parse and validate receipt
    receipt = parse_receipt(data)

    # Generate unique ID
    receipt_id = str(uuid4())

    # Store receipt
    receipt_store[receipt_id] = receipt

    # Calculate points
    points = calculate_points(receipt)
    receipt_points_store[receipt_id] = points

    # Return receipt ID
    return jsonify({"id": receipt_id})

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_receipt_points(receipt_id):
    # Retrieve points
    points = receipt_points_store.get(receipt_id)
    
    # Check if receipt exists
    if points is None:
        return NotFound('No receipt found for that id')

    # Return points
    return jsonify({"points": points})

if __name__ == '__main__':
    app.run()
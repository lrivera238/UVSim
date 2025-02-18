from flask import Blueprint, request, jsonify
from models.uvsim_model import UVSimModel
from services.uvsim_service import UVSimService

uvsim_api = Blueprint('uvsim_api', __name__)

# Initialize model and service
uvsim_model = UVSimModel()
uvsim_service = UVSimService(uvsim_model)

@uvsim_api.route('/load_memory', methods=['POST'])
def load_memory():
    """Load a set of instructions into memory."""
    data = request.json.get('instructions', [])
    uvsim_service.load_to_memory(data)
    return jsonify({"message": "Memory loaded successfully"}), 200

@uvsim_api.route('/execute', methods=['POST'])
def execute():
    """Execute instructions in memory."""
    result = uvsim_service.execute()
    return jsonify({"message": result}), 200

@uvsim_api.route('/reset', methods=['POST'])
def reset():
    """Reset the UVSim state."""
    uvsim_model.reset()
    return jsonify({"message": "Simulator reset"}), 200

@uvsim_api.route('/read', methods=['POST'])
def read():
    """Simulate a READ operation."""
    operand = request.json.get('operand')
    value = request.json.get('value')
    try:
        uvsim_service.read(operand, value)
        return jsonify({"message": "Value stored successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@uvsim_api.route('/write/<operand>', methods=['GET'])
def write(operand):
    """Simulate a WRITE operation."""
    try:
        value = uvsim_service.write(operand)
        return jsonify({"value": value}), 200
    except IndexError:
        return jsonify({"error": "Invalid memory address"}), 400

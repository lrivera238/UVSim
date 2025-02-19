from flask import Blueprint, request, jsonify
from Model.UVSimModel import UVSimModel
from Services.UVSimService import UVSimService


uvsim_api = Blueprint('uvsim_api', __name__)

# Initialize model and service
uvsim_model = UVSimModel()
uvsim_service = UVSimService(uvsim_model)

#memory
@uvsim_api.route('/get_memory', methods=['GET'])
def get_memory():
    """Returns the current memory state."""
    return jsonify({"memory": uvsim_model.memory}), 200

def update_memory():
    """Updates a specific memory location."""
    data = request.json
    address = int(data.get('address'))
    value = data.get('value')

    # Validate memory address
    if address < 0 or address >= len(uvsim_model.memory):
        return jsonify({"error": "Invalid memory address"}), 400

    # Store the new value in memory
    uvsim_model.memory[address] = value
    return jsonify({"message": f"Memory[{address}] updated to {value}"}), 200

@uvsim_api.route('/load_memory', methods=['POST'])
def load_memory():
    """Load a set of instructions into memory."""
    data = request.json.get('instructions', [])
    uvsim_service.load_to_memory(data)
    return jsonify({"message": "Memory loaded successfully"}), 200

# accumulator   
@uvsim_api.route('/get_accumulator', methods=['GET'])
def get_accumulator():
    """Returns the current value of the accumulator."""
    return jsonify({"accumulator": uvsim_model.accumulator}), 200
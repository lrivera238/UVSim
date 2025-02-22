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

# def update_memory():
#     """Updates a specific memory location."""
#     data = request.json
#     address = int(data.get('address'))
#     value = data.get('value')

#     # Validate memory address
#     if address < 0 or address >= len(uvsim_model.memory):
#         return jsonify({"error": "Invalid memory address"}), 400

#     # Store the new value in memory
#     uvsim_model.memory[address] = value
#     return jsonify({"message": f"Memory[{address}] updated to {value}"}), 200

@uvsim_api.route('/load_memory', methods=['POST'])
def load_memory():
    """Load a set of instructions into memory."""
    data = request.json.get('instructions', [])
    uvsim_service.load_to_memory(data)
    return jsonify({"message": "Memory loaded successfully"}), 200

@uvsim_api.route('/update_memory', methods=['POST'])
def update_memory():
    """Updates a specific memory location."""
    data = request.json
    address = int(data.get('address'))
    value = data.get('value')

    # Validate memory address
    if address < 0 or address >= len(uvsim_model.memory):
        return jsonify({"error": "Invalid memory address"}), 400

    # Validate memory format (+0000 to +9999 and -0000 to -9999)
    if not isinstance(value, str) or len(value) != 5 or (value[0] not in ['+', '-']) or not value[1:].isdigit():
        return jsonify({"error": "Invalid memory format. Must be +0000 to +9999 or -0000 to -9999"}), 400

    # Store the new value in memory
    uvsim_model.memory[address] = value
    return jsonify({"message": f"Memory[{address}] updated to {value}"}), 200


# accumulator   
@uvsim_api.route('/get_status', methods=['GET'])
def get_status():
    """Returns the values of the accumulator and instruction pointer."""
    return jsonify({
        "accumulator": uvsim_model.accumulator,
        "instruction_pointer": uvsim_model.instruction_pointer
    }), 200
    
# instructions
@uvsim_api.route('/step_instruction', methods=['POST'])
def step_instruction():
    """Executes the next instruction. If input is required, waits for user input."""
    data = request.json
    user_input = data.get("input")  # User input (if provided)

    result = uvsim_service.step_instruction(user_input)
    return jsonify(result), 200

@uvsim_api.route('/load_file', methods=['POST'])
def load_file():
    """Loads a file into memory, ensuring valid formatting."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    content = file.read().decode('utf-8-sig')  # Read as UTF-8, removing BOM

    # Normalize line endings and remove hidden characters
    instructions = [line.strip() for line in content.splitlines() if line.strip()]

    # Load into memory
    uvsim_service.load_to_memory(instructions)

    return jsonify({"message": "File loaded into memory successfully"}), 200

# general
@uvsim_api.route('/reset', methods=['POST'])
def reset_system():
    """Resets the UVSim system to its initial state."""
    result = uvsim_service.reset()
    return jsonify(result), 200



from flask import Blueprint, request, jsonify, session
from Model.UVSimModel import UVSimModel
from Services.UVSimService import UVSimService
import uuid

uvsim_api = Blueprint('uvsim_api', __name__)

# Dictionary to store UVSim instances
uvsim_instances = {}

def get_active_instance():
    """Get or create the active UVSim instance for the current tab"""
    # Check different possible sources for tab_id
    tab_id = None
    
    # Check URL parameters
    tab_id = request.args.get('tab_id')
    
    # Check JSON body if no tab_id in URL
    if not tab_id and request.is_json:
        tab_id = request.json.get('tab_id')
        
    # Check form data if no tab_id found yet
    if not tab_id and request.form:
        tab_id = request.form.get('tab_id')
    
    if not tab_id or tab_id not in uvsim_instances:
        return None
    
    return uvsim_instances[tab_id]

@uvsim_api.route('/create_instance', methods=['POST'])
def create_instance():
    """Create a new UVSim instance and return its ID"""
    tab_id = str(uuid.uuid4())
    uvsim_model = UVSimModel()
    uvsim_service = UVSimService(uvsim_model)
    uvsim_instances[tab_id] = {
        'model': uvsim_model,
        'service': uvsim_service,
        'name': request.json.get('name', f'Program {len(uvsim_instances) + 1}')
    }
    
    return jsonify({
        "tab_id": tab_id,
        "name": uvsim_instances[tab_id]['name']
    }), 200

@uvsim_api.route('/list_instances', methods=['GET'])
def list_instances():
    """List all available UVSim instances"""
    instances = [{
        "tab_id": tab_id,
        "name": instance['name']
    } for tab_id, instance in uvsim_instances.items()]
    
    return jsonify({"instances": instances}), 200

@uvsim_api.route('/rename_instance', methods=['POST'])
def rename_instance():
    """Rename a UVSim instance"""
    tab_id = request.json.get('tab_id')
    new_name = request.json.get('name')
    
    if not tab_id or tab_id not in uvsim_instances:
        return jsonify({"error": "Instance not found"}), 404
        
    if not new_name:
        return jsonify({"error": "No name provided"}), 400
        
    uvsim_instances[tab_id]['name'] = new_name
    return jsonify({"message": "Instance renamed successfully"}), 200

@uvsim_api.route('/delete_instance', methods=['POST'])
def delete_instance():
    """Delete a UVSim instance"""
    tab_id = request.json.get('tab_id')
    
    if not tab_id or tab_id not in uvsim_instances:
        return jsonify({"error": "Instance not found"}), 404
        
    del uvsim_instances[tab_id]
    return jsonify({"message": "Instance deleted successfully"}), 200

#memory
@uvsim_api.route('/get_memory', methods=['GET'])
def get_memory():
    """Returns the current memory state."""
    instance = get_active_instance()
    if not instance:
        return jsonify({"error": "No active instance"}), 400
        
    return jsonify({"memory": instance['model'].memory}), 200

@uvsim_api.route('/load_memory', methods=['POST'])
def load_memory():
    """Load a set of instructions into memory."""
    instance = get_active_instance()
    if not instance:
        return jsonify({"error": "No active instance"}), 400
        
    data = request.json.get('instructions', [])
    instance['service'].load_to_memory(data)
    return jsonify({"message": "Memory loaded successfully"}), 200

@uvsim_api.route('/update_memory', methods=['POST'])
def update_memory():
    """Updates a specific memory location."""
    instance = get_active_instance()
    if not instance:
        return jsonify({"error": "No active instance"}), 400
        
    data = request.json
    address = int(data.get('address'))
    value = data.get('value')

    # Validate memory address
    if address < 0 or address >= len(instance['model'].memory):
        return jsonify({"error": "Invalid memory address"}), 400

    # Validate memory format (+0000 to +9999 and -0000 to -9999)
    if not isinstance(value, str) or len(value) != 5 or (value[0] not in ['+', '-']) or not value[1:].isdigit():
        return jsonify({"error": "Invalid memory format. Must be +0000 to +9999 or -0000 to -9999"}), 400

    # Store the new value in memory
    instance['model'].memory[address] = value
    return jsonify({"message": f"Memory[{address}] updated to {value}"}), 200


# accumulator   
@uvsim_api.route('/get_status', methods=['GET'])
def get_status():
    """Returns the values of the accumulator and instruction pointer."""
    instance = get_active_instance()
    if not instance:
        return jsonify({"error": "No active instance"}), 400
        
    return jsonify({
        "accumulator": instance['model'].accumulator,
        "instruction_pointer": instance['model'].instruction_pointer
    }), 200
    
# instructions
@uvsim_api.route('/step_instruction', methods=['POST'])
def step_instruction():
    """Executes the next instruction. If input is required, waits for user input."""
    instance = get_active_instance()
    if not instance:
        return jsonify({"error": "No active instance"}), 400
        
    data = request.json
    user_input = data.get("input")  # User input (if provided)

    result = instance['service'].step_instruction(user_input)
    return jsonify(result), 200

@uvsim_api.route('/load_file', methods=['POST'])
def load_file():
    """Loads a file into memory and immediately returns a response."""
    instance = get_active_instance()
    if not instance:
        return jsonify({"error": "No active instance"}), 400
        
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    content = file.read().decode('utf-8-sig')  # Read as UTF-8, removing BOM

    # Normalize line endings and remove hidden characters
    instructions = [line.strip() for line in content.splitlines() if line.strip()]

    # Check if there are more than 100 commands (excluding -99999)
    command_count = sum(1 for instr in instructions if instr != '-99999')
    if command_count > 100:
        # Reset the system to clear memory
        instance['service'].reset()
        return jsonify({
            "error": "Program too long",
            "message": f"Error: Cannot load program. You attempted to load {command_count} commands, but the maximum allowed is 100."
        }), 400

    # Load into memory
    instance['service'].load_to_memory(instructions)

    # Force update of memory in the response
    updated_memory = instance['model'].memory  # Get latest memory after load

    return jsonify({
        "message": "File loaded into memory successfully",
        "memory": updated_memory
    }), 200

# general
@uvsim_api.route('/reset', methods=['POST'])
def reset_system():
    """Resets the UVSim system to its initial state."""
    instance = get_active_instance()
    if not instance:
        return jsonify({"error": "No active instance"}), 400
        
    result = instance['service'].reset()
    return jsonify(result), 200
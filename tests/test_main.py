import unittest
from unittest.mock import patch, mock_open
from Model.UVSimModel import UVSimModel
from Services.UVSimService import UVSimService

class TestUVSim(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.model = UVSimModel()
        self.service = UVSimService(self.model)
    
    def reset_system(self):
        """Reset the system to initial state."""
        self.model.reset()
        
    def generate_large_file(self, lines=150):
        """Generate a mock file with more than 100 lines of instructions."""
        return "\n".join([f"+030{str(i).zfill(2)}" for i in range(lines)]) + "\n"
    
    # Use case 1 Load Program into Memory
    def test_memory_initialized(self):
        self.reset_system()
        self.assertEqual(self.model.memory[0], "+000000")
        self.service.load_to_memory(["+03002", "+04300"])
        self.assertEqual(self.model.memory[0], "+03002")
        
    def test_memory_not_initialized(self):
        self.reset_system()
        self.assertEqual(self.model.memory[0], "+000000")
        try:
            self.service.load_to_memory([])
        except:
            pass
        self.assertEqual(self.model.memory[0], "+000000")
    
    # Use case 2 Execute Program
    def test_execute_program(self):
        self.reset_system()
        # Using the full 7-character format for each instruction
        self.model.memory[0] = "+030015"  # Add contents of memory location 15 to accumulator
        self.model.memory[1] = "+043000"  # Halt
        self.model.memory[15] = "+000015" # Value 15 stored at memory location 15
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 15)
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        
    def test_execute_program_invalid_instruction(self):
        self.reset_system()
        self.model.memory[0] = "+0301515"  # Too long for valid instruction (8 chars)
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)

    # Use case 3 Handle I/O Operations
    def test_Read_valid_input(self):
        self.reset_system()
        self.model.memory[0] = "+010002"  # Read into memory location 2
        result = self.service.step_instruction("1234")
        self.assertEqual(self.model.memory[2], "+001234")

    def test_Read_invalid_input(self):
        self.reset_system()
        self.model.memory[0] = "+010002"
        with self.assertRaises(ValueError):
            self.service.step_instruction("notanumber")

    def test_Read_invalid_range_input(self):
        self.reset_system()
        self.model.memory[0] = "+010002"
        with self.assertRaises(ValueError):
            self.service.step_instruction("2000000")  # Exceeds 6-digit limit

    def test_Write(self):
        self.reset_system()
        self.model.memory[0] = "+011003"  # Write from memory location 3
        self.model.memory[3] = "+005678"
        result = self.service.step_instruction()
        self.assertEqual(result.get("message"), "Output: 5678")

    def test_Write_Negative(self):
        self.reset_system()
        self.model.memory[0] = "+011003"
        self.model.memory[3] = "-005678"
        result = self.service.step_instruction()
        self.assertEqual(result.get("message"), "Output: -5678")
        
    # Use case 4 Perform Arithmetic Operations
    def test_Add(self):
        self.reset_system()
        self.model.memory[0] = "+030001"  # Add contents of memory location 1
        self.model.memory[1] = "+000004"  # Value 4 stored at memory location 1
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 4)
        
    def test_Subtract(self):
        self.reset_system()
        self.model.memory[0] = "+031001"  # Subtract contents of memory location 1
        self.model.memory[1] = "+000004"  # Value 4 stored at memory location 1
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, -4)
        
        self.reset_system()
        self.model.memory[0] = "+031001"
        self.model.memory[1] = "+000004"
        self.model.accumulator = 10
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 6)
        
    def test_Multiply(self):
        self.reset_system()
        self.model.memory[0] = "+033005"  # Multiply accumulator by contents of memory location 5
        self.model.memory[5] = "+000004"  # Value 4 stored at memory location 5
        self.model.accumulator = 5
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 20)
        
    def test_Divide(self):
        self.reset_system()
        self.model.memory[0] = "+032005"  # Divide accumulator by contents of memory location 5
        self.model.memory[5] = "+000004"  # Value 4 stored at memory location 5
        self.model.accumulator = 20
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 5)

    # Use case 5 Store and Load Data
    def test_Load(self):
        self.reset_system()
        self.model.memory[0] = "+020004"  # Load contents of memory location 4 into accumulator
        self.model.memory[4] = "+004321"  # Value 4321 stored at memory location 4
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 4321)

    def test_Load_Negative(self):
        self.reset_system()
        self.model.memory[0] = "+020004"
        self.model.memory[4] = "-004321"
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, -4321)

    def test_Store(self):
        self.reset_system()
        self.model.accumulator = 9999
        self.model.memory[0] = "+021005"  # Store accumulator in memory location 5
        result = self.service.step_instruction()
        self.assertEqual(self.model.memory[5], "+009999")

    def test_Store_Negative(self):
        self.reset_system()
        self.model.accumulator = -9999
        self.model.memory[0] = "+021005"
        result = self.service.step_instruction()
        self.assertEqual(self.model.memory[5], "-009999")
        
    # Use case 6 Implement Control Flow
    def test_Branch(self):
        self.reset_system()
        self.model.memory[0] = "+040005"  # Branch to memory location 5
        result = self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 5)
        
    def test_BranchNeg(self):
        self.reset_system()
        self.model.accumulator = -1
        self.model.memory[0] = "+041005"  # Branch to memory location 5 if accumulator is negative
        result = self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 5)
        
        self.reset_system()
        self.model.accumulator = 1
        self.model.memory[0] = "+041005"
        result = self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 1)
        
    def test_BranchZero(self):
        self.reset_system()
        self.model.accumulator = 0
        self.model.memory[0] = "+042005"  # Branch to memory location 5 if accumulator is zero
        result = self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 5)
        
        self.reset_system()
        self.model.accumulator = 1
        self.model.memory[0] = "+042005"
        result = self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 1)
    
    # Use case 7 Halt Execution
    def test_Halt_Before_Add(self):
        self.reset_system()
        self.model.memory[0] = "+043000"  # Halt
        self.model.memory[1] = "+030015"  # Add (never executed)
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)
        self.assertEqual(self.model.instruction_pointer, 0)
        
    def test_Halt_After_Add(self):
        self.reset_system()
        self.model.memory[0] = "+030015"  # Add contents of memory location 15 to accumulator
        self.model.memory[15] = "+000015"  # Value 15 stored at memory location 15
        self.model.memory[1] = "+043000"  # Halt
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 15)
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.instruction_pointer, 1)
    
    # Use case 8 Detect and Report Errors
    def test_Invalid_Operand(self):
        self.reset_system()
        self.model.memory[0] = "+0301515"  # Too long (8 chars)
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)
        self.assertEqual(self.model.instruction_pointer, 0)
        
    def test_Invalid_Instruction(self):
        self.reset_system()
        self.model.memory[0] = "+090015"  # Invalid opcode 090
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)
        self.assertEqual(self.model.instruction_pointer, 0)
    
    # Use case 9 Handle Memory Limits
    def test_Memory_Limit(self):
        self.reset_system()
        instructions = [f"+030{str(i).zfill(2)}" for i in range(300)]
        self.service.load_to_memory(instructions)
        self.assertEqual(len(self.model.memory), 250)  # Model should have 250 memory slots
        
    def test_Memory_Load_Limit(self):
        self.reset_system()
        instructions = [f"+030{str(i).zfill(2)}" for i in range(300)]
        self.service.load_to_memory(instructions)
        with self.assertRaises(IndexError):
            _ = self.model.memory[250]  # Accessing beyond the 250 memory limit
    
    # Use case 10 Read from an Input File
    def test_Read_From_Input_File(self):
        self.reset_system()
        self.service.load_to_memory(["+03002", "+04300"])
        result = self.service.step_instruction()
        self.assertEqual(self.model.memory[0], "+03002")
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))

if __name__ == "__main__":
    unittest.main()

# Run the tests with the following command:
# python -m unittest discover tests

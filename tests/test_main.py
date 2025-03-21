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
        return "\n".join([f"+30{str(i).zfill(2)}" for i in range(lines)]) + "\n"
    
    # Use case 1 Load Program into Memory
    def test_memory_initialized(self):
        self.reset_system()
        self.assertEqual(self.model.memory[0], "+0000")
        self.service.load_to_memory(["+3002", "+4300"])
        self.assertEqual(self.model.memory[0], "+3002")
        
    def test_memory_not_initialized(self):
        self.reset_system()
        self.assertEqual(self.model.memory[0], "+0000")
        try:
            self.service.load_to_memory([])
        except:
            pass
        self.assertEqual(self.model.memory[0], "+0000")
    
    # Use case 2 Execute Program
    def test_execute_program(self):
        self.reset_system()
        self.model.memory[0] = "+3015"
        self.model.memory[1] = "+4300"
        self.model.memory[15] = "+0015"
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 15)
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        
    def test_execute_program_invalid_instruction(self):
        self.reset_system()
        self.model.memory[0] = "+30151"
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)

    # Use case 3 Handle I/O Operations
    def test_Read_valid_input(self):
        self.reset_system()
        self.model.memory[0] = "+1002"
        result = self.service.step_instruction("1234")
        self.assertEqual(self.model.memory[2], "+1234")

    def test_Read_invalid_input(self):
        self.reset_system()
        self.model.memory[0] = "+1002"
        with self.assertRaises(ValueError):
            self.service.step_instruction("notanumber")

    def test_Read_invalid_range_input(self):
        self.reset_system()
        self.model.memory[0] = "+1002"
        with self.assertRaises(ValueError):
            self.service.step_instruction("20000")

    def test_Write(self):
        self.reset_system()
        self.model.memory[0] = "+1103"
        self.model.memory[3] = "+5678"
        result = self.service.step_instruction()
        self.assertEqual(result.get("message"), "Output: 5678")

    def test_Write_Negative(self):
        self.reset_system()
        self.model.memory[0] = "+1103"
        self.model.memory[3] = "-5678"
        result = self.service.step_instruction()
        self.assertEqual(result.get("message"), "Output: -5678")
        
    # Use case 4 Perform Arithmetic Operations
    def test_Add(self):
        self.reset_system()
        self.model.memory[0] = "+3001"  # Add from memory[1]
        self.model.memory[1] = "+0004"  # Value to add
        self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 4)
        
    def test_Subtract(self):
        self.reset_system()
        self.model.memory[0] = "+3101"  # Subtract from memory[1]
        self.model.memory[1] = "+0004"  # Value to subtract
        self.service.step_instruction()
        self.assertEqual(self.model.accumulator, -4)
        
        self.reset_system()
        self.model.memory[0] = "+3101"  # Subtract from memory[1]
        self.model.memory[1] = "+0004"  # Value to subtract
        self.model.accumulator = 10
        self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 6)
        
    def test_Multiply(self):
        self.reset_system()
        self.model.memory[5] = "+0004"
        self.model.accumulator = 5
        self.model.memory[0] = "+3305"
        self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 20)
        
    def test_Divide(self):
        self.reset_system()
        self.model.memory[5] = "+0004"
        self.model.accumulator = 20
        self.model.memory[0] = "+3205"
        self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 5)

    # Use case 5 Store and Load Data
    def test_Load(self):
        self.reset_system()
        self.model.memory[4] = "+4321"
        self.model.memory[0] = "+2004"
        self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 4321)

    def test_Load_Negative(self):
        self.reset_system()
        self.model.memory[4] = "-4321"
        self.model.memory[0] = "+2004"
        self.service.step_instruction()
        self.assertEqual(self.model.accumulator, -4321)

    def test_Store(self):
        self.reset_system()
        self.model.accumulator = 9999
        self.model.memory[0] = "+2105"
        self.service.step_instruction()
        self.assertEqual(self.model.memory[5], "+9999")

    def test_Store_Negative(self):
        self.reset_system()
        self.model.accumulator = -9999
        self.model.memory[0] = "+2105"
        self.service.step_instruction()
        self.assertEqual(self.model.memory[5], "-9999")
        
    # Use case 6 Implement Control Flow
    def test_Branch(self):
        self.reset_system()
        self.model.memory[0] = "+4005"
        self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 5)
        
    def test_BranchNeg(self):
        self.reset_system()
        self.model.accumulator = -1
        self.model.memory[0] = "+4105"
        self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 5)
        
        self.reset_system()
        self.model.accumulator = 1
        self.model.memory[0] = "+4105"
        self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 1)
        
    def test_BranchZero(self):
        self.reset_system()
        self.model.accumulator = 0
        self.model.memory[0] = "+4205"
        self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 5)
        
        self.reset_system()
        self.model.accumulator = 1
        self.model.memory[0] = "+4205"
        self.service.step_instruction()
        self.assertEqual(self.model.instruction_pointer, 1)
    
    # Use case 7 Halt Execution
    def test_Halt_Before_Add(self):
        self.reset_system()
        self.model.memory[0] = "+4300"
        self.model.memory[1] = "+3015"
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)
        self.assertEqual(self.model.instruction_pointer, 0)
        
    def test_Halt_After_Add(self):
        self.reset_system()
        self.model.memory[0] = "+3015"
        self.model.memory[15] = "+0015"
        self.model.memory[1] = "+4300"
        result = self.service.step_instruction()
        self.assertEqual(self.model.accumulator, 15)
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.instruction_pointer, 1)
    
    # Use case 8 Detect and Report Errors
    def test_Invalid_Operand(self):
        self.reset_system()
        self.model.memory[0] = "+30151"
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)
        self.assertEqual(self.model.instruction_pointer, 0)
        
    def test_Invalid_Instruction(self):
        self.reset_system()
        self.model.memory[0] = "+9015"
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))
        self.assertEqual(self.model.accumulator, 0)
        self.assertEqual(self.model.instruction_pointer, 0)
    
    # Use case 9 Handle Memory Limits
    def test_Memory_Limit(self):
        self.reset_system()
        instructions = [f"+30{str(i).zfill(2)}" for i in range(150)]
        self.service.load_to_memory(instructions)
        self.assertEqual(len(self.model.memory), 100)
        
    def test_Memory_Load_Limit(self):
        self.reset_system()
        instructions = [f"+30{str(i).zfill(2)}" for i in range(150)]
        self.service.load_to_memory(instructions)
        with self.assertRaises(IndexError):
            _ = self.model.memory[100]
    
    # Use case 10 Read from an Input File
    def test_Read_From_Input_File(self):
        self.reset_system()
        self.service.load_to_memory(["+3002", "+4300"])
        result = self.service.step_instruction()
        self.assertEqual(self.model.memory[0], "+3002")
        result = self.service.step_instruction()
        self.assertTrue(result.get("halt", False))

if __name__ == "__main__":
    unittest.main()

# Run the tests with the following command:
# python -m unittest discover tests

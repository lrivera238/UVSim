import unittest
from unittest.mock import patch
import main  # Importing main.py to test its functions

class TestUVSim(unittest.TestCase):
    
    def reset_main(self):
        main.accumulator = 0
        main.instruction_pointer = 0
        main.memory = [""] * 100
    
    # Use case 1 Load Program into Memory
    def test_memory_initialized(self):
        self.reset_main()
        self.assertTrue(main.memory[0] == "")
        main.load_to_memory("tests/Test1.txt")
        self.assertTrue(main.memory[0] != "")
        
    def test_memory_not_initialized(self):
        self.reset_main()
        self.assertTrue(main.memory[0] == "")
        try:
            main.load_to_memory("tests/Test2.txt")
        except:
            pass
        self.assertTrue(main.memory[0] == "")
    
    # Use case 2 Execute Program
    def test_execute_program(self):
        self.reset_main()
        main.memory[0] = "+3015"
        main.execute_instructions()
        self.assertTrue(main.accumulator == 15)
        
    def test_execute_program_invalid_instruction(self):
        self.reset_main()
        main.memory[0] = "+30151"
        main.execute_instructions()
        self.assertTrue(main.accumulator == 0)

    # Use case 3 Handle I/O Operations
    @patch('builtins.input', return_value='1234')
    def test_Read_valid_input(self, mock_input):
        main.Read(2)
        self.assertEqual(main.memory[2], 1234)

    @patch('builtins.input', return_value='notanumber')
    def test_Read_invalid_input(self, mock_input):
        with self.assertRaises(ValueError):  # Expecting ValueError
            main.Read(2)

    @patch('builtins.input', return_value='20000')
    def test_Read_invalid_range_input(self, mock_input):
        with self.assertRaises(ValueError):  # Expecting ValueError
            main.Read(2)

    @patch('builtins.print')
    def test_Write(self, mock_print):
        main.memory[3] = 5678
        main.Write(3)
        mock_print.assert_called_once_with(5678)

    @patch('builtins.print')
    def test_Write_Negative(self, mock_print):
        main.memory[3] = -5678
        main.Write(3)
        mock_print.assert_called_once_with(-5678)
        
    # Use case 4 Perform Arithmetic Operations
    def test_Add(self):
        self.reset_main()
        main.Add(4)
        self.assertEqual(main.accumulator, 4)
        
    def test_Subtract(self):
        self.reset_main()
        main.Subtract(4)
        self.assertEqual(main.accumulator, -4)
        
        self.reset_main()
        main.accumulator = 10
        main.Subtract(4)
        self.assertEqual(main.accumulator, 6)

    # Use case 5 Store and Load Data
    def test_Load(self):
        main.memory[4] = 4321
        main.Load(4)
        self.assertEqual(main.accumulator, 4321)

    def test_Load_Negative(self):
        main.memory[4] = -4321
        main.Load(4)
        self.assertEqual(main.accumulator, -4321)


    def test_Store(self):
        main.accumulator = 9999
        main.Store(5)
        self.assertEqual(main.memory[5], 9999)

    def test_Store_Negative(self):
        main.accumulator = -9999
        main.Store(5)
        self.assertEqual(main.memory[5], -9999)
        
    # Use case 6 Implement Control Flow
    
    # Use case 7 Halt Execution
    
    # Use case 8 Detect and Report Errors
    
    # Use case 9 Handle Memory Limits
    
    # Use case 10 Read from an Input File

if __name__ == "__main__":
    unittest.main()

# Run the tests with the following command:
# python -m unittest discover tests

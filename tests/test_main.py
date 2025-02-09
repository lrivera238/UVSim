import unittest
from unittest.mock import patch, mock_open
import main  # Importing main.py to test its functions

class TestUVSim(unittest.TestCase):
    
    def reset_main(self):
        main.accumulator = 0
        main.instruction_pointer = 0
        main.memory = [""] * 100
        
    def generate_large_file(self, lines=150):
        """Generate a mock file with more than 100 lines of instructions."""
        return "\n".join([f"+30{str(i).zfill(2)}" for i in range(lines)]) + "\n"
    
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
        main.memory[1] = "+4300"
        main.memory[15] = 15
        with self.assertRaises(SystemExit):
            main.execute_instructions()
        self.assertTrue(main.accumulator == 15)
        
    def test_execute_program_invalid_instruction(self):
        self.reset_main()
        main.memory[0] = "+30151"
        with self.assertRaises(SystemExit):
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
        main.memory[0] = 4
        main.Add("00")
        self.assertEqual(main.accumulator, 4)
        
    def test_Subtract(self):
        self.reset_main()
        main.memory[0] = 4
        main.Subtract("00")
        self.assertEqual(main.accumulator, -4)
        
        self.reset_main()
        main.memory[0] = 4
        main.accumulator = 10
        main.Subtract("00")
        self.assertEqual(main.accumulator, 6)
        
    def test_Multiply(self):
        self.reset_main()
        main.memory[5] = 4
        main.accumulator = 5
        main.Multiply("05")
        self.assertEqual(main.accumulator, 20)
        
    def test_Divide(self):
        self.reset_main()
        main.memory[5] = 4
        main.accumulator = 20
        main.Divide("05")
        self.assertEqual(main.accumulator, 5)

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
    def test_Branch(self):
        self.reset_main()
        main.Branch("05")
        self.assertEqual(main.instruction_pointer, 5)
        
    def test_BranchNeg(self):
        self.reset_main()
        main.accumulator = -1
        main.BranchNeg("05")
        self.assertEqual(main.instruction_pointer, 5)
        
        self.reset_main()
        main.accumulator = 1
        main.BranchNeg("05")
        self.assertEqual(main.instruction_pointer, 0)
        
    def test_BranchZero(self):
        self.reset_main()
        main.accumulator = 0
        main.BranchZero("05")
        self.assertEqual(main.instruction_pointer, 5)
        
        self.reset_main()
        main.accumulator = 1
        main.BranchZero("05")
        self.assertEqual(main.instruction_pointer, 0)
    
    # Use case 7 Halt Execution
    def test_Halt_Before_Add(self):
        self.reset_main()
        main.memory[0] = "+4300"
        main.memory[1] = "+3015"
        with self.assertRaises(SystemExit):
            main.execute_instructions()
        self.assertEqual(main.accumulator, 0)
        self.assertEqual(main.instruction_pointer, 0)
        
    def test_Halt_After_Add(self):
        self.reset_main()
        main.memory[0] = "+3015"
        main.memory[15] = 15
        main.memory[1] = "+4300"
        with self.assertRaises(SystemExit):
            main.execute_instructions()
        self.assertEqual(main.accumulator, 15)
        self.assertEqual(main.instruction_pointer, 1)
    
    # Use case 8 Detect and Report Errors
    def test_Invalid_Operand(self):
        self.reset_main()
        main.memory[0] = "+30151"
        with self.assertRaises(SystemExit):
            main.execute_instructions()
        self.assertEqual(main.accumulator, 0)
        self.assertEqual(main.instruction_pointer, 0)
        
    def test_Invalid_Instruction(self):
        self.reset_main()
        main.memory[0] = "+9015"
        with self.assertRaises(SystemExit):
            main.execute_instructions()
        self.assertEqual(main.accumulator, 0)
        self.assertEqual(main.instruction_pointer, 0)
    
    # Use case 9 Handle Memory Limits
    @patch("builtins.open", new_callable=mock_open)
    def test_Memory_Limit(self, mock_file):
        self.reset_main()
        
        # Simulate a file with 150 lines
        mock_file.return_value.read.return_value = self.generate_large_file(150)

        main.load_to_memory("mock_file.txt")  
        main.execute_instructions()
        self.assertEqual(len(main.memory), 100) 
        self.assertEqual(main.instruction_pointer, 100)
        
    @patch("builtins.open", new_callable=mock_open)
    def test_Memory_Load_Limit(self, mock_file):
        self.reset_main()
        mock_file.return_value.read.return_value = self.generate_large_file(150)
        main.load_to_memory("mock_file.txt")  
        self.assertNotIn(100, main.memory)  # Memory[100] should not exist
    
    # Use case 10 Read from an Input File
    def test_Read_From_Input_File(self):
        self.reset_main()  # Reset UVSim state
        main.load_to_memory("tests/Test1.txt")
        with self.assertRaises(SystemExit):
                main.execute_instructions()
        self.assertEqual(main.memory[0], "+3002")
        self.assertEqual(main.memory[1], "+4300")
    

if __name__ == "__main__":
    unittest.main()

# Run the tests with the following command:
# python -m unittest discover tests

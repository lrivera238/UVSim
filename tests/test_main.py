import unittest
import main  # Importing main.py to test its functions

class TestUVSim(unittest.TestCase):
    
    def test_memory_initialized(self):
        self.assertTrue(main.memory[0] == "")
        main.load_to_memory("tests/Test1.txt")
        self.assertTrue(main.memory[0] != "")
        
    def test_memory_not_initialized(self):
        self.assertTrue(main.memory[0] == "")
        try:
            main.load_to_memory("tests/Test2.txt")
        except:
            pass
        self.assertTrue(main.memory[0] == "")
        
    def test_execute_program(self):
        main.accumulator = 0
        main.memory[0] = "+3015"
        main.execute_instructions()
        self.assertTrue(main.accumulator == 15)
        
    def test_execute_program_invalid_instruction(self):
        main.accumulator = 0
        main.memory[0] = "+30151"
        main.execute_instructions()
        self.assertTrue(main.accumulator == 0)

if __name__ == "__main__":
    unittest.main()

# Run the tests with the following command:
# python -m unittest discover tests

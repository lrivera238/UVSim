import unittest
import main  # Importing main.py to test its functions

class TestUVSim(unittest.TestCase):
    
    def test_memory_initialized(self):
        self.assertTrue(main.memory[0] == "")
        main.load_to_memory("tests/Test1.txt")
        self.assertTrue(main.memory[0] != "")
        
    def test_memory_not_initialized(self):
        self.assertTrue(main.memory[0] == "")
        main.load_to_memory("tests/Test2.txt")
        self.assertTrue(main.memory[0] == "")

if __name__ == "__main__":
    unittest.main()

# Run the tests with the following command:
# python -m unittest discover tests

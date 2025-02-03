import unittest
import main  # Importing main.py to test its functions

class TestUVSim(unittest.TestCase):
    def setUp(self):
        main.memory = [0] * 100
        main.accumulator = 0
        
if __name__ == "__main__":
    unittest.main()
    
# Run the tests with the following command:
# python -m unittest discover tests

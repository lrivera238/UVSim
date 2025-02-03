# run_tests.py
import unittest

if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.TestLoader().discover("tests"))

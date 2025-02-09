# UVSim

## Overview
UVSim is a simple stored-program computer simulator written in Python. It reads BasicML instructions from a file and executes them.

## Requirements
- Python 3 installed on your system.
- A text file containing valid UVSim instructions.

## How to Run

1. Open a terminal or command prompt.

2. Navigate to the directory where "main.py" is located.

3. Run the program using Python.
   --python main.py

4. Enter the file name when prompted.
   - The program will ask for the file that contains the instructions.
   - Example input: "instructions.txt"

5. The program will execute the instructions if the file exists.
   - If the file is not found, an error message will be displayed.
   
## Example Usage
$ python main.py
Enter the instruction file name: instructions.txt
Executing instructions...
Done.

## Notes
- Ensure the instruction file is in the same directory as `main.py`, or provide the full path when prompted.
- The instruction file must follow the correct format expected by UVSim.

## Troubleshooting
- File not found: Check if you entered the correct filename and path.
- Syntax errors in instructions: Ensure the instruction file follows the expected format.
- Python not recognized: If you get a "python is not recognized" error, try using "python3 main.py" instead.
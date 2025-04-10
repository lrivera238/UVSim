# UVSim - Universal Virtual Machine Simulator

## Overview

UVSim is a web-based simulator for a basic machine language.

Access the application at: [https://uvsim-426884250334.us-central1.run.app/]

Access the code base at: [https://github.com/lrivera238/UVSim/]

## Using the UVSim Application

### Memory View

The center of the interface displays the UVSim's memory contents:

- Each memory location shows its address and current value
- Memory values can be edited directly by clicking on them and entering a new value
- Valid memory values must be in the format of '+NNNN' or '-NNNN' (where N is a digit)
- The currently executing instruction is highlighted

### Status Display

The right side shows the current state of the UVSim:

- **Accumulator**: Shows the current value stored in the accumulator
- **Instruction Pointer**: Shows the address of the next instruction to be executed

### Execution Console

Below the status display is the execution console that shows:

- Program output from WRITE instructions
- Error messages
- Execution status messages

### Control Buttons

- **Run**: Executes the program continuously until completion or until input is required
- **Step**: Executes a single instruction and then pauses
- **Reset**: Resets the UVSim to its initial state (clears memory, accumulator, and instruction pointer)
- **Choose File**: Opens a file dialog to choose a program
- **Load File**: Loads the chosen program
- **Save**: Saves the current program to a file
- **Theme**: Toggles between light and dark theme

### Loading a Program

To load a program into UVSim:

1. Click the "Choose File" button
2. Select a text file containing UVSim instructions
3. Click the "Load File" button
4. Each line in the file should contain one instruction in the format '+NNNN'
5. The program will be loaded into memory starting at address 0

### Manual Program Entry

You can also enter a program manually:

1. Click on any memory location in the memory display
2. Enter the instruction value in the format '+NNNN'
3. Repeat for each instruction in your program

### Executing a Program

To run a program:

1. Load the program into memory
2. Click "Run" to execute continuously or "Step" to execute one instruction at a time

When a program requires input (READ operation):

1. A dialog box will appear
2. Enter the required integer value
3. Click "Submit" to continue execution

### Understanding Instruction Format

UVSim instructions are 4-digit numbers with a leading sign:

- First two digits (after the sign): Operation code (opcode)
- Last two digits: Operand address

### Instruction Set

UVSim supports the following instructions:

| Code | Operation | Description |
|------|-----------|-------------|
| 10   | READ      | Read a value from input into a memory location |
| 11   | WRITE     | Write a value from a memory location to output |
| 20   | LOAD      | Load a value from memory into the accumulator |
| 21   | STORE     | Store the accumulator value into memory |
| 30   | ADD       | Add a value from memory to the accumulator |
| 31   | SUBTRACT  | Subtract a value from memory from the accumulator |
| 32   | DIVIDE    | Divide the accumulator by a value from memory |
| 33   | MULTIPLY  | Multiply the accumulator by a value from memory |
| 40   | BRANCH    | Jump to a specified memory location |
| 41   | BRANCHNEG | Jump if accumulator is negative |
| 42   | BRANCHZERO| Jump if accumulator is zero |
| 43   | HALT      | Stop program execution |

### Saving a Program

To save your current program:

1. Click the "Save" button
2. Choose a location and filename for your program
3. The program will be saved as a text file with one instruction per line
4. The saved file can be loaded later using the "Load File" button

### Customizing the Interface

To change themes:
1. Click the "Adjust color" button
2. You will be prompted to enter 4 hexadecimal color values in this order:
   - First color: Main backdrop color (--backdrop)
   - Second color: Secondary background color (--background)
   - Third color: Primary color for main elements (--primary)
   - Fourth color: Secondary color for secondary elements (--secondary)
3. Each color can be entered with or without the '#' prefix
4. Colors must be valid 6-digit hexadecimal values (e.g., "FF0000" or "#FF0000" for red)

## Troubleshooting

If you encounter issues:

1. **Invalid Input**: Ensure all memory values follow the +/-NNNN format
2. **Program Not Running**: Check that the instruction pointer is at the first instruction
3. **Unexpected Results**: Use the "Step" button to execute one instruction at a time and observe the accumulator and memory changes
4. **Page Not Loading**: Try refreshing the page or clearing your browser cache

## Technical Requirements

The UVSim web application should work in any modern web browser:
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Safari

No installation is required as this is a web-based application.

## Limitations

- Memory is limited to 100 locations (00-99)
- Values must be between -9999 and +9999
- Only integer arithmetic is supported
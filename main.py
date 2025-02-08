memory = ["" for _ in range(100)]
accumulator = 0
instruction_pointer = 0

def Read(opperand):
    data = input("Please enter an input line: ")
    try:
        data = int(data)
    except ValueError:
        raise ValueError("Invalid input")
    if data % 10000 != 0:
        raise ValueError("Invalid input")
    memory[opperand] = data

def Write(opperand):
    print(memory[opperand])

def Load(opperand):
    accumulator = memory[opperand]

def Store(opperand):
    memory[opperand] = accumulator

def Add(opperand):
    global accumulator
    accumulator += int(opperand)
    
def Subtract(opperand):
    global accumulator
    accumulator -= int(opperand)

def Branch(operand):
    global instruction_pointer
    instruction_pointer = int(operand)

def BranchNeg(operand):
    global instruction_pointer
    if accumulator < 0:
        instruction_pointer = int(operand)

def BranchZero(operand):
    global instruction_pointer
    if accumulator == 0:
        instruction_pointer = int(operand)

def Halt():
    print("Program halted.")
    exit()
    
def load_to_memory(file_path):
    global memory, instruction_pointer
    with open(file_path, "r") as file:
        for line in file:
            try:
                line = line.rstrip("\n")
                memory[instruction_pointer] = line
                instruction_pointer += 1
                if instruction_pointer >= 100:
                    print("You've entered more than 100 commands, programm terminated")
                    return
            except ValueError:
                print(f"Invalid instruction {line} on line {instruction_pointer + 1}")
                return
    instruction_pointer = 0
    
def execute_instructions():
    global memory, instruction_pointer
     # Execute each instruction   
    while instruction_pointer < len(memory):
        if len(memory[instruction_pointer]) > 5:
            print(f"Invalid instruction {memory[instruction_pointer]} on line {instruction_pointer + 1}")
            return
        try:
            sign = memory[instruction_pointer][0]
            instruction = memory[instruction_pointer][1:3]
            operand = memory[instruction_pointer][3:]
        except:
            instruction_pointer += 1
            continue
        
        if sign == "-":
            print(f"Invalid instruction {memory[instruction_pointer]} on line {instruction_pointer + 1}")
            return
        if instruction == "00" and operand == "00":
            continue
        
        match instruction:
            case "10":
                print(operand)
                # Read(opperand)
            case "11":
                print(operand)
                # Write(opperand)
            case "20":
                print(operand)
                # Load(opperand)
            case "21":
                print(operand)
                # Store(opperand)
            case "30":
                Add(operand)
            case "31":
                Subtract(operand)
            case "32":
                print(operand)
                # Divide(opperand)
            case "33":
                print(operand)
                # Multiply(opperand)
            case "40":
                print(operand)
                # Branch(opperand)
            case "41":
                print(operand)
                # BranchNeg(opperand)
            case "42":
                print(operand)
                # BranchZero(opperand)
            case "43":
                Halt()
                return
            case _:
                print(f"Invalid instruction {line} on line {instruction_pointer + 1}")
                return
            
        instruction_pointer += 1
        

def main():
    global memory, accumulator, instruction_pointer
    file_path = input("Enter the file path: ")
    
    # Load file into memory
    load_to_memory(file_path)
    
    # Execute each instruction
    execute_instructions()
            
    print("End of program reached without HALT")

if __name__ == "__main__":
    main()
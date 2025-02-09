memory = ["" for _ in range(100)]
accumulator = 0
instruction_pointer = 0

def Read(operand):
    data = input("Please enter an input line: ")
    try:
        data = int(data)  # Convert input to integer
    except ValueError:
        raise ValueError("Invalid input: must be an integer")

    # Validate that the number is within the four-digit signed range (-9999 to 9999)
    if not (-9999 <= data <= 9999):
        raise ValueError("Invalid input: must be a four-digit signed number (-9999 to 9999)")

    memory[int(operand)] = data  # Store in memory

def Write(operand):
    print(memory[int(operand)])

def Load(operand):
    global accumulator
    accumulator = memory[int(operand)]

def Store(operand):
    global accumulator
    memory[int(operand)] = accumulator

def Add(operand):
    global accumulator, memory
    accumulator += int(memory[int(operand)])
    
def Subtract(operand):
    global accumulator, memory
    accumulator -= int(memory[int(operand)])
    
def Divide(operand):
    global accumulator, memory
    accumulator /= int(memory[int(operand)])
    
def Multiply(operand):
    global accumulator, memory
    accumulator *= int(memory[int(operand)])

def Branch(operand):
    global instruction_pointer
    instruction_pointer = int(operand)

def BranchNeg(operand):
    global instruction_pointer
    if accumulator < 0:
        instruction_pointer = int(operand)
        return True

def BranchZero(operand):
    global instruction_pointer
    if accumulator == 0:
        instruction_pointer = int(operand)
        return True

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
                    exit()
            except ValueError:
                print(f"Invalid instruction {line} on line {instruction_pointer + 1}")
                exit()
    instruction_pointer = 0
    
def execute_instructions():
    global memory, instruction_pointer
     # Execute each instruction   
    while instruction_pointer < len(memory):
        if len(memory[instruction_pointer]) > 5:
            print(f"Invalid instruction {memory[instruction_pointer]} on line {instruction_pointer + 1}")
            exit()
        try:
            sign = memory[instruction_pointer][0]
            instruction = memory[instruction_pointer][1:3]
            operand = memory[instruction_pointer][3:]
        except:
            instruction_pointer += 1
            continue
        
        if sign == "-":
            print(f"Invalid instruction {memory[instruction_pointer]} on line {instruction_pointer + 1}")
            exit()
        if instruction == "00" and operand == "00":
            continue
        
        match instruction:
            case "10":
                Read(operand)
            case "11":
                Write(operand)
            case "20":
                Load(operand)
            case "21":
                Store(operand)
            case "30":
                Add(operand)
            case "31":
                Subtract(operand)
            case "32":
                Divide(operand)
            case "33":
                Multiply(operand)
            case "40":
                Branch(operand)
                continue
            case "41":
                if BranchNeg(operand):
                    continue
            case "42":
                if BranchZero(operand):
                    continue
            case "43":
                Halt()
            case _:
                print(f"Invalid instruction {memory[instruction_pointer]} on line {instruction_pointer + 1}")
                exit()
            
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
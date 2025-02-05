# Main():
# 	Ask user for file path and store it in variable file_path
#     Open file at file_path
#     If file does not exist:
#         Display error and terminate program

#     Initialize memory as an array of size 100 // This will need to be a global variable
#     Initialize accumulator (register) // This will need to be a global variable
#     Initialize instruction_pointer to 0 // This will need to be a global variable

#     For each line in the file:
#         If line is valid:
#             Convert line to integer
#             Store the instruction in memory at instruction_pointer
#             Increment instruction_pointer
#         Else:
#             Display error and terminate program

#     Set instruction_pointer to 0

#     While instruction_pointer is within memory bounds:
#         Fetch instruction from memory at instruction_pointer
#         Decode the instruction into opcode and operand
#         If opcode is HALT:
#             Terminate program
#         Else:
#             Execute the function for opcode using operand
#         Increment instruction_pointer

#     Display message: "End of program reached without HALT"

memmory = [0] * 100
accumulator = 0
instruction_pointer = 0

def main():
    file_path = input("Enter the file path: ")
    print(file_path)

if __name__ == "__main__":
    main()
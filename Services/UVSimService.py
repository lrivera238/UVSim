from .ArithmeticOperations import ArithmeticOperations
from .MemoryOperations import MemoryOperations
from .BranchOperations import BranchOperations

class UVSimService:
    def __init__(self, model):
        self.model = model
        self.arithmetic = ArithmeticOperations(model)
        self.memory = MemoryOperations(model)
        self.branch = BranchOperations(model)

    def halt(self):
        """Halt execution."""
        return "Program halted."

    def load_to_memory(self, instructions):
        """Load a list of instructions into memory."""
        self.model.reset()
        # Only load up to 250 instructions
        for index, line in enumerate(instructions[:250]):
            self.model.memory[index] = line
            
    def reset(self):
        """Resets memory, accumulator, and instruction pointer to initial state."""
        self.model.reset()
        return {"message": "System reset successful."}

    def step_instruction(self, user_input=None):
        """Executes the next instruction in memory."""
        if self.model.instruction_pointer >= len(self.model.memory):
            return {"message": "End of program reached without HALT", "halt": True}

        instruction = self.model.memory[self.model.instruction_pointer]
        if not instruction or len(instruction) != 7:
            # This is where we'd convert the old 4 length (a + or -, followed by two digits for opcode, followed by 2 digits for operand) to the new 6 length format. One length was added to opcode and operand.
            return {"message": f"Invalid instruction {instruction} at {self.model.instruction_pointer}", "halt": True}

        sign = instruction[0]
        opcode = instruction[1:4]
        operand = instruction[4:]

        if sign == "-":
            return {"message": f"Invalid instruction {instruction} at {self.model.instruction_pointer}", "halt": True}

        match opcode:
            case "010":  # Read
                if user_input is None:
                    return {"message": f"Input required for memory[{operand}]", "waitForInput": True}
                # Let ValueError propagate up for invalid input
                self.memory.read(operand, user_input)
                self.model.instruction_pointer += 1
                return {"message": f"Read {user_input} into memory[{operand}]"}

            case "11":  # Write
                self.model.instruction_pointer += 1
                return {"message": f"Output: {self.memory.write(operand)}"}

            case "020":  # Load
                self.memory.load(operand)
            case "021":  # Store
                self.memory.store(operand)
            case "030":  # Add
                self.arithmetic.add(operand)
            case "031":  # Subtract
                self.arithmetic.subtract(operand)
            case "032":  # Divide
                self.arithmetic.divide(operand)
            case "033":  # Multiply
                self.arithmetic.multiply(operand)
            case "040":  # Branch
                self.branch.branch(operand)
                return {"message": f"Branched to {operand}"}
            case "041":  # Branch if Negative
                if self.branch.branch_neg(operand):
                    return {"message": f"Branching to {operand} because accumulator is negative"}
            case "042":  # Branch if Zero
                if self.branch.branch_zero(operand):
                    return {"message": f"Branching to {operand} because accumulator is zero"}
            case "043":  # Halt
                return {"message": "Program halted.", "halt": True}
            case _:
                return {"message": f"Invalid instruction {instruction} at {self.model.instruction_pointer}", "halt": True}

        self.model.instruction_pointer += 1
        if self.model.instruction_pointer >= len(self.model.memory):
            return {"message": "End of program reached without HALT", "halt": True}
        return {"message": f"Executed instruction {instruction}. Pointer at {self.model.instruction_pointer}"}


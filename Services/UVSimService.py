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
        # Only load up to 100 instructions
        for index, line in enumerate(instructions[:100]):
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
        if not instruction or len(instruction) != 5:
            return {"message": f"Invalid instruction {instruction} at {self.model.instruction_pointer}", "halt": True}

        sign = instruction[0]
        opcode = instruction[1:3]
        operand = instruction[3:]

        if sign == "-":
            return {"message": f"Invalid instruction {instruction} at {self.model.instruction_pointer}", "halt": True}

        match opcode:
            case "10":  # Read
                if user_input is None:
                    return {"message": f"Input required for memory[{operand}]", "waitForInput": True}
                # Let ValueError propagate up for invalid input
                self.memory.read(operand, user_input)
                self.model.instruction_pointer += 1
                return {"message": f"Read {user_input} into memory[{operand}]"}

            case "11":  # Write
                self.model.instruction_pointer += 1
                return {"message": f"Output: {self.memory.write(operand)}"}

            case "20":  # Load
                self.memory.load(operand)
            case "21":  # Store
                self.memory.store(operand)
            case "30":  # Add
                self.arithmetic.add(operand)
            case "31":  # Subtract
                self.arithmetic.subtract(operand)
            case "32":  # Divide
                self.arithmetic.divide(operand)
            case "33":  # Multiply
                self.arithmetic.multiply(operand)
            case "40":  # Branch
                self.branch.branch(operand)
                return {"message": f"Branched to {operand}"}
            case "41":  # Branch if Negative
                if self.branch.branch_neg(operand):
                    return {"message": f"Branching to {operand} because accumulator is negative"}
            case "42":  # Branch if Zero
                if self.branch.branch_zero(operand):
                    return {"message": f"Branching to {operand} because accumulator is zero"}
            case "43":  # Halt
                return {"message": "Program halted.", "halt": True}
            case _:
                return {"message": f"Invalid instruction {instruction} at {self.model.instruction_pointer}", "halt": True}

        self.model.instruction_pointer += 1
        if self.model.instruction_pointer >= len(self.model.memory):
            return {"message": "End of program reached without HALT", "halt": True}
        return {"message": f"Executed instruction {instruction}. Pointer at {self.model.instruction_pointer}"}


class UVSimService:
    def __init__(self, model):
        self.model = model

    def read(self, operand, value):
        """Simulate reading an input."""
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Invalid input: must be an integer")

        if not (-9999 <= value <= 9999):
            raise ValueError("Invalid input: must be within (-9999 to 9999)")

        self.model.memory[int(operand)] = value

    def write(self, operand):
        """Retrieve a value from memory."""
        return self.model.memory[int(operand)]

    def load(self, operand):
        """Load a value into the accumulator."""
        self.model.accumulator = int(self.model.memory[int(operand)])

    def store(self, operand):
        """Store the accumulator value into memory."""
        self.model.memory[int(operand)] = self.model.accumulator

    def add(self, operand):
        """Add a value to the accumulator."""
        self.model.accumulator += int(self.model.memory[int(operand)])

    def subtract(self, operand):
        """Subtract a value from the accumulator."""
        self.model.accumulator -= int(self.model.memory[int(operand)])

    def divide(self, operand):
        """Divide the accumulator by a value."""
        divisor = int(self.model.memory[int(operand)])
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.model.accumulator /= divisor

    def multiply(self, operand):
        """Multiply the accumulator by a value."""
        self.model.accumulator *= int(self.model.memory[int(operand)])

    def branch(self, operand):
        """Branch unconditionally."""
        self.model.instruction_pointer = int(operand)

    def branch_neg(self, operand):
        """Branch if accumulator is negative."""
        if self.model.accumulator < 0:
            self.model.instruction_pointer = int(operand)
            return True
        return False

    def branch_zero(self, operand):
        """Branch if accumulator is zero."""
        if self.model.accumulator == 0:
            self.model.instruction_pointer = int(operand)
            return True
        return False

    def halt(self):
        """Halt execution."""
        return "Program halted."

    def load_to_memory(self, instructions):
        """Load a list of instructions into memory."""
        self.model.reset()
        for index, line in enumerate(instructions):
            self.model.memory[index] = line
            
    def reset(self):
        """Resets memory, accumulator, and instruction pointer to initial state."""
        self.model.reset()
        return {"message": "System reset successful."}

    def step_instruction(self, user_input=None): #This used to be execute()
        """Executes the next instruction in memory. If input is required, it waits for user input."""
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
            case "10":  # Read (Requires input)
                if user_input is None:
                    return {"message": f"Input required for memory[{operand}]", "waitForInput": True}

                try:
                    self.read(operand, user_input)
                except ValueError as e:
                    return {"message": f"Error: {str(e)}", "halt": True}

            case "11":  # Write
                return {"message": f"Output: {self.write(operand)}"}

            case "20":  # Load
                self.load(operand)
            case "21":  # Store
                self.store(operand)
            case "30":  # Add
                self.add(operand)
            case "31":  # Subtract
                self.subtract(operand)
            case "32":  # Divide
                self.divide(operand)
            case "33":  # Multiply
                self.multiply(operand)
            case "40":  # Branch
                self.branch(operand)
                return {"message": f"Branched to {operand}"}
            case "41":  # Branch if Negative
                if self.branch_neg(operand):
                    return {"message": f"Branching to {operand} because accumulator is negative"}
            case "42":  # Branch if Zero
                if self.branch_zero(operand):
                    return {"message": f"Branching to {operand} because accumulator is zero"}
            case "43":  # Halt
                return {"message": "Program halted.", "halt": True}
            # case _:
                # return {"message": f"Invalid instruction {instruction} at {self.model.instruction_pointer}", "halt": True}

        self.model.instruction_pointer += 1  # Move to the next instruction
        if self.model.instruction_pointer >= len(self.model.memory):
            return {"message": "End of program reached without HALT", "halt": True}
        return {"message": f"Executed instruction {instruction}. Pointer at {self.model.instruction_pointer}"}


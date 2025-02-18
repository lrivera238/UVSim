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

    def execute(self):
        """Execute loaded instructions."""
        while self.model.instruction_pointer < len(self.model.memory):
            instruction = self.model.memory[self.model.instruction_pointer]
            if not instruction or len(instruction) != 5:
                break  # Stop execution on empty or malformed instruction

            sign = instruction[0]
            opcode = instruction[1:3]
            operand = instruction[3:]

            if sign == "-":
                return f"Invalid instruction {instruction} at {self.model.instruction_pointer}"

            match opcode:
                case "10":
                    return "Input required"
                case "11":
                    return self.write(operand)
                case "20":
                    self.load(operand)
                case "21":
                    self.store(operand)
                case "30":
                    self.add(operand)
                case "31":
                    self.subtract(operand)
                case "32":
                    self.divide(operand)
                case "33":
                    self.multiply(operand)
                case "40":
                    self.branch(operand)
                    continue
                case "41":
                    if self.branch_neg(operand):
                        continue
                case "42":
                    if self.branch_zero(operand):
                        continue
                case "43":
                    return self.halt()
                case _:
                    return f"Invalid instruction {instruction} at {self.model.instruction_pointer}"

            self.model.instruction_pointer += 1

        return "End of program reached without HALT"

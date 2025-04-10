class MemoryOperations:
    def __init__(self, model):
        self.model = model

    def read(self, operand, value):
        """Simulate reading an input."""
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Invalid input: must be an integer")

        if not (-999999 <= value <= 999999):
            raise ValueError("Invalid input: must be within (-999999 to 999999)")

        if int(operand) > 249 or int(operand) < 0:
            raise ValueError("Invalid input: provided memory address must be within (0 to 249)")
        
        self.model.memory[int(operand)] = self.model.format_value(value)

    def write(self, operand):
        """Retrieve a value from memory."""

        if int(operand) > 249 or int(operand) < 0:
            raise ValueError("Invalid input: provided memory address must be within (0 to 249)")
        
        memory_value = self.model.memory[int(operand)]
        if isinstance(memory_value, str) and len(memory_value) == 7:
            sign = 1 if memory_value[0] == "+" else -1
            return sign * int(memory_value[1:])
        return memory_value

    def load(self, operand):
        """Load a value into the accumulator."""

        if int(operand) > 249 or int(operand) < 0:
            raise ValueError("Invalid input: provided memory address must be within (0 to 249)")
        
        self.model.accumulator = int(self.model.memory[int(operand)])

    def store(self, operand):
        """Store the accumulator value into memory."""

        if int(operand) > 249 or int(operand) < 0:
            raise ValueError("Invalid input: provided memory address must be within (0 to 249)")
        
        self.model.memory[int(operand)] = self.model.format_value(self.model.accumulator) 
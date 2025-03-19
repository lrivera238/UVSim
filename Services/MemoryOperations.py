class MemoryOperations:
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

        self.model.memory[int(operand)] = self.model.format_value(value)

    def write(self, operand):
        """Retrieve a value from memory."""
        memory_value = self.model.memory[int(operand)]
        if isinstance(memory_value, str) and len(memory_value) == 5:
            sign = 1 if memory_value[0] == "+" else -1
            return sign * int(memory_value[1:])
        return memory_value

    def load(self, operand):
        """Load a value into the accumulator."""
        self.model.accumulator = int(self.model.memory[int(operand)])

    def store(self, operand):
        """Store the accumulator value into memory."""
        self.model.memory[int(operand)] = self.model.format_value(self.model.accumulator) 
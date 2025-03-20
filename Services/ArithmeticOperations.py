class ArithmeticOperations:
    def __init__(self, model):
        self.model = model

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
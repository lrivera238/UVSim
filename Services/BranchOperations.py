class BranchOperations:
    def __init__(self, model):
        self.model = model

    def branch(self, operand):
        """Branch unconditionally."""
        if int(operand) > 249 or int(operand) < 0:
            raise ValueError("Invalid input: provided memory address must be within (0 to 249)")
        self.model.instruction_pointer = int(operand)

    def branch_neg(self, operand):
        """Branch if accumulator is negative."""
        if int(operand) > 249 or int(operand) < 0:
            raise ValueError("Invalid input: provided memory address must be within (0 to 249)")
        if self.model.accumulator < 0:
            self.model.instruction_pointer = int(operand)
            return True
        return False

    def branch_zero(self, operand):
        """Branch if accumulator is zero."""
        if int(operand) > 249 or int(operand) < 0:
            raise ValueError("Invalid input: provided memory address must be within (0 to 249)")
        if self.model.accumulator == 0:
            self.model.instruction_pointer = int(operand)
            return True
        return False 
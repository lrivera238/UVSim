class BranchOperations:
    def __init__(self, model):
        self.model = model

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
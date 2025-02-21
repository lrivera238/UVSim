class UVSimModel:
    def __init__(self):
        self.memory = ["+0000" for _ in range(100)]
        self.accumulator = 0
        self.instruction_pointer = 0
    
    def reset(self):
        self.memory = ["+0000" for _ in range(100)]
        self.accumulator = 0
        self.instruction_pointer = 0
from src.Standard import Turing

class Multi_Tape_Turing(Turing):
    def __init__(self, tolerance, num_tape):
        super().__init__(tolerance, num_tape)
        self.type = 'MTAPE'
        self.num_tape = num_tape

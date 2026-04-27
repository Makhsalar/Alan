from src.Standard import Turing

class Multi_Tape_Turing(Turing):
    def __init__(self, speed, tolerance):
        super().__init__(speed, tolerance)
        self.type = 'MTAPE'
        # Under Construction

from Standard import Turing

class Stay_Turing(Turing):
    def __init__(self, speed, tolerance):
        super().__init__(speed, tolerance)
        self.allowed_moves.append('S')

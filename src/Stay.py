from src.Standard import Turing

class Stay_Turing(Turing):
    def __init__(self, tolerance):
        super().__init__(tolerance)
        self.type = 'STAY'
        self.allowed_moves.append('S')

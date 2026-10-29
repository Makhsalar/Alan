from src.Standard import Turing

class Non_Deterministic_Turing(Turing):
    def __init__(self, tolerance):
        super().__init__(tolerance)
        self.type = 'NON'
        # Under Construction

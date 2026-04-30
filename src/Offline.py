from src.Standard import Turing

class Offline_Turing(Turing):
    def __init__(self, tolerance):
        super().__init__(tolerance)
        self.type = 'OFFL'
        # Under Construction

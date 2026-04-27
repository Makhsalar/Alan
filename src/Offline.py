from Standard import Turing

class Offline_Turing(Turing):
    def __init__(self, speed, tolerance):
        super().__init__(speed, tolerance)
        self.type = 'OFFL'
        # Under Construction

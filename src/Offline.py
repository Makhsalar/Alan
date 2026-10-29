import csv
from src.Standard import Turing
from src.Tape import Tape

class Offline_Turing(Turing):
    def __init__(self, tolerance):
        super().__init__(tolerance, num_tape=2)
        self.type = 'OFFL'
        # Under Construction

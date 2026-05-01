from src.Standard import Turing

class Multi_Dimension_Turing(Turing):
    def __init__(self, tolerance, dim):
        super().__init__(tolerance)
        self.type = 'MDIM'
        self.dim = dim
        # Under Construction

from src.Standard import Turing


class Stay_Turing(Turing):
    def __init__(self, tolerance: int) -> None:
        super().__init__(tolerance)
        self.type = "STAY"
        self.allowed_moves = self.allowed_moves + ["S"]

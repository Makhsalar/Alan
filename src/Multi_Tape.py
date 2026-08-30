from src.Standard import Turing


class Multi_Tape_Turing(Turing):
    def __init__(self, tolerance: int, num_tape: int) -> None:
        super().__init__(tolerance, num_tape)
        self.type = "MTAPE"
        self.num_tape = num_tape


class Multi_Tape_Stay_Turing(Multi_Tape_Turing):
    def __init__(self, tolerance: int, num_tape: int) -> None:
        super().__init__(tolerance, num_tape)
        self.type = "SMTAPE"
        self.allowed_moves = self.allowed_moves + ["S"]

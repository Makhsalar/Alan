from src.Standard import Turing


class Semi_Infinite_Turing(Turing):
    def __init__(self, tolerance: int) -> None:
        super().__init__(tolerance)
        self.type = "SINF"

    def apply_move(self, move: str, tape_index: int) -> None:
        match move:
            case "R":
                self.tape[tape_index].move_right()
            case "L":
                if self.tape[tape_index].position <= 0:
                    return
                return self.tape[tape_index].move_left()
            case _:
                return

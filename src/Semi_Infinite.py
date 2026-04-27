from Standard import Turing
from src.Terminal import Colors

class Semi_Infinite_Turing(Turing):
    def __init__(self, speed, tolerance):
        super().__init__(speed, tolerance)
        self.type = 'SINF'
    
    def apply_move(self, move):
        match move:
            case 'R':
                self.tape.move_right()
            case 'L':
                if self.tape.position <= 0:
                    return
                return self.tape.move_left()
            case _:
                return

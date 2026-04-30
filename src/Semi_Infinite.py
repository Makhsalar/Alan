from src.Standard import Turing

class Semi_Infinite_Turing(Turing):
    def __init__(self, tolerance):
        super().__init__(tolerance)
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

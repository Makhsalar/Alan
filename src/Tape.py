from collections import defaultdict


class Tape:
    def __init__(self, blank: str = "_"):  # ∅
        self.blank: str = blank
        self.tape: defaultdict[int, str] = defaultdict(lambda: blank)
        self.position: int = 0

    def read(self) -> str:
        return self.tape[self.position]

    def write(self, symbol: str) -> None:
        self.tape[self.position] = symbol

    def move_left(self) -> None:
        self.position -= 1

    def move_right(self) -> None:
        self.position += 1

    def __str__(self) -> str:
        if self.tape:
            indices = self.tape.keys()
            low, high = min(indices), max(indices)
        else:
            low, high = 0, 0

        cells: list[str] = []
        for cell in range(low, high + 1):
            if cell == self.position:
                cells.append(f"|[{self.tape[cell]}]|")
            else:
                cells.append(f"| {self.tape[cell]} |")
        return "".join(cells)

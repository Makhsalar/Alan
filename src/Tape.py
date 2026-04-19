from collections import defaultdict

class Tape:
    def __init__(self, blank='∅'):
        self.blank = blank
        self.tape = defaultdict(lambda: blank)
        self.position = 0

    def read(self):
        return self.tape[self.position]

    def write(self, symbol):
        self.tape[self.position] = symbol

    def move_left(self):
        self.position -= 1

    def move_right(self):
        self.position += 1

    def __str__(self):
        if self.tape:
            indices = self.tape.keys()
            low, high = min(indices), max(indices)
        else:
            low, high = 0, 0

        cells = []
        for i in range(low, high + 1):
            if i == self.position:
                cells.append(f'|[{self.tape[i]}]|')
            else:
                cells.append(f'| {self.tape[i]} |')
        return ''.join(cells)

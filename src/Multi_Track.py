import csv
from typing import Any

from src.Standard import Turing


class Multi_Track_Turing(Turing):
    def __init__(self, tolerance: int, num_tape: int) -> None:
        super().__init__(tolerance, num_tape)
        self.type = "MTRK"
        self.num_tape = num_tape

    def fetch_transitions(self) -> None:
        with open("transitions.csv", "r") as TTABLE:
            reader = csv.reader(TTABLE)
            for transition in reader:
                source_node = transition[0]
                edge: dict[str, Any] = {}

                for idx in range(self.num_tape):
                    edge[f"read{idx}"] = transition[2 * idx + 1]
                    edge[f"write{idx}"] = transition[2 * idx + 2]
                    # In MTRK, there is only one move column at index 2 * self.num_tape + 1
                    # We broadcast this single move to all virtual "tapes" (tracks)
                    edge[f"move{idx}"] = transition[2 * self.num_tape + 1]

                edge["destination_node"] = transition[-1]

                if source_node not in self.states:
                    self.states[source_node] = self.Node(
                        name=source_node,
                        next_states={transition[-1]},
                        edges=[edge],
                    )
                else:
                    self.states[source_node].next_states.add(transition[-1])
                    if edge not in self.states[source_node].edges:
                        self.states[source_node].edges.append(edge)

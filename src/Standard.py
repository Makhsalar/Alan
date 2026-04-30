import csv
from time import sleep
from src.Tape import Tape

class Turing:
    class Node:
        def __init__(
                self,
                name = 'q0',
                next_states = set(),
                edges = [],
                ):
            self.name = name
            self.next_states = next_states
            self.edges = edges     


        def __str__(self):
            return self.name
     
    def __init__(self, tolerance=10000, num_tape=1):
        self.name = 'default'
        self.num_tape = 1
        self.step_counter = 0
        self.tolerance = tolerance
        self.allowed_moves = ['R', 'L']
        self.states = dict()
        self.start_state = self.Node()
        self.final_state = None
        self.type = 'STD'
        self.num_tape = 1
        self.input_string = {}
        self.alphabet = {}
        self.gamma = {}
        self.tape = {}
        self.tape_log = {}
        self.idx_range = range(0, 3 * self.num_tape, 3)
        for idx in range(self.num_tape):
            self.input_string[idx] = ''
            self.alphabet[idx] = []
            self.gamma[idx] = []
            self.tape[idx] = Tape()
            self.tape_log[idx] = []

    def get_machine_type(self):
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                if i == 1:
                    if len(line) > 2 and line[2].strip():
                        self.type = line[2].strip()
                        return line[2].strip()
        return 'STD'

    def fetch_data(self):
        with open('data.csv', 'r') as DATA:
            reader = csv.reader(DATA)
            for line in reader:
                if reader.line_num == 1:
                    self.name = line[0]
                    for idx in self.idx_range:
                        index = idx // 3
                        self.input_string[index] = line[idx + 1]
                        for char in self.input_string[index]:
                            self.tape[index].write(char)
                            self.tape[index].move_right()
                        self.tape[index].position = 0
                        self.alphabet[index] = list(line[idx + 2].split('-'))
                        self.gamma[index] = list(line[idx + 3].split('-'))
                
                elif reader.line_num == 2:
                    self.start_state = self.Node(name=line[0])
                    self.final_state = self.Node(name=line[1])
                    self.states[self.start_state.name] = self.start_state
                    self.states[self.final_state.name] = self.final_state
                    self.current_state = self.start_state

    def fetch_transitions(self):
        with open('transitions.csv', 'r') as TTABLE:
            reader = csv.reader(TTABLE)
            for transition in reader:
                source_node = transition[0]
                if source_node not in self.states:
                    edge = {}
                    for idx in self.idx_range:
                        index = idx // 3
                        edge[f'read{index}'] = transition[idx + 1]
                        edge[f'write{index}'] = transition[idx + 2]
                        edge[f'move{index}'] = transition[idx + 3]
                    edge['destination_node'] = transition[-1]
                    self.states[source_node] = self.Node(
                        name = source_node,
                        next_states = set([transition[-1]]),
                        edges = [edge],
                        )
                else:
                    self.states[source_node].next_states.add(transition[-1])
                    edge = {}
                    for idx in self.idx_range:
                        index = idx // 3
                        edge[f'read{index}'] = transition[idx + 1]
                        edge[f'write{index}'] = transition[idx + 2]
                        edge[f'move{index}'] = transition[idx + 3]
                    edge['destination_node'] = transition[-1]
                    if edge not in self.states[source_node].edges:
                        self.states[source_node].edges.append(edge)

    def halt(self):
        if self.current_state == self.final_state:
            print('Input is accepted')
        else:
            print('Input is rejected')
        print(f'current state: {self.current_state}')
        if self.step_counter == self.tolerance:
            print('Maximum Limit Of Steps Reached')
        else:
            print(f'Total Steps: {self.step_counter}')
        exit()

    def input_is_valid(self):
        for inp in self.input_string:
            for item in list(self.input_string[inp]):
                if item not in self.alphabet[inp]:
                    print(f'{item} not available in Σ{inp}')
                    self.halt()
        return True

    def check_integrity_of_edges(self, edges):
        boolean = []
        for index in range(self.num_tape):
            r = [edge[f'read{index}'] for edge in edges]
            w = [edge[f'write{index}'] for edge in edges]
            m = [edge[f'move{index}'] for edge in edges]
            for item in r:
                if item not in self.gamma[index]:
                    print(f'{item} (read char) is not available in Γ{index}')
                    self.halt()
            for item in w:
                if item not in self.gamma[index]:
                    print(f'{item} (write char) is not available in Γ{index}')
                    self.halt()
            for item in m:
                if item not in self.allowed_moves:
                    print(f'{item} is not available in move set of tape')
                    self.halt()
            boolean.append(len(r) == len(set(r)))

        return all(boolean)
        
    def apply_move(self, move, tape_index):
        match move:
            case 'R':
                self.tape[tape_index].move_right()
            case 'L':
                return self.tape[tape_index].move_left()
            case _:
                return
            
    def apply_transition(self, edges):
        for edge in edges:
            all_match = True
            for idx in range(self.num_tape):
                if self.tape[idx].read() != edge[f'read{idx}']:
                    all_match = False
                    break
            if all_match:
                for idx in range(self.num_tape):
                    self.tape[idx].write(edge[f'write{idx}'])
                    self.apply_move(move=edge[f'move{idx}'], tape_index=idx)
                self.current_state = self.states[edge['destination_node']]
                self.step_counter += 1
                return
        self.halt()

    def visualize(self):
        visualize = {'y': True, 'n': False}[input('Do you wish to see the tape? (y/n): ').lower()]
        if visualize:
            speed = float(input('Enter Speed Of Visualization Of Tape (Recommended = 0.7s): '))
            for idx, tape in enumerate(zip(*self.tape_log.values())):
                print(f'Step {idx}:')
                for t in tape:
                    print(t)
                print()
                sleep(speed)

    def process_input(self):
        if self.input_string:
            checked_nodes = set()
            while (self.current_state != self.final_state) and (self.step_counter < self.tolerance):
                edges = self.current_state.edges
                for key in list(self.tape.keys()):
                    self.tape_log[key].append(str(self.tape[key]))
                if self.current_state not in checked_nodes:
                    if self.check_integrity_of_edges(edges):
                        checked_nodes.add(self.current_state)
                        self.apply_transition(edges)
                    else:
                        print(f'Invalid edges on {self.current_state}')
                        self.visualize()
                        self.halt()
                else:
                    self.apply_transition(edges)
        self.visualize()
        self.halt()

    def run(self):
        self.fetch_data()
        self.fetch_transitions()
        print(self.name)
        print(f'Machine Type: {self.type}')
        print(f'Σ: {self.alphabet}')
        print(f'Γ: {self.gamma}')
        self.input_is_valid()
        print(f'Input: {self.input_string}')
        self.process_input()
        
    def __str__(self):
        return self.name

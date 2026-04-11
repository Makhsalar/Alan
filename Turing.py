import csv
from Tape import visualize_tape

size = int(input('Enter Size Of The Tape: '))
tolerance = int(input('Enter Maximum Steps of Machine: '))
speed = float(input('Enter Speed Of Visualization Of Tape (Recommended = 0.7s): '))

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
     
    def __init__(self):
        self.name = 'default'
        self.input_string = ''
        self.alphabet = []
        self.gamma = []
        self.tape = []
        self.allowed_moves = ['R', 'L']
        self.states = dict()
        self.head = 0
        self.start_state = self.Node()
        self.final_state = None
        self.step_counter = 0

    def fetch_data(self):
        with open('data.csv', 'r') as DATA:
            reader = csv.reader(DATA)
            for line in reader:
                if reader.line_num == 1:
                    self.name = line[0]
                    self.input_string = line[1]
                    self.tape = list(line[1])
                    self.tape.extend(['∅' for _ in range(size - len(line[1]))])
                    self.alphabet = list(line[2].split('-'))
                    self.gamma = list(line[3].split('-'))
                
                elif reader.line_num == 2:
                    self.start_state = self.Node(name=line[0])
                    self.final_state = self.Node(name=line[1])
                    self.states[self.start_state.name] = self.start_state
                    self.states[self.final_state.name] = self.final_state
                    self.current_state = self.start_state

            DATA.close()

    def fetch_transitions(self):
        with open('transitions.csv', 'r') as TTABLE:
            reader = csv.reader(TTABLE)
            for transition in reader:
                source_node = transition[0]
                if source_node not in self.states:
                    self.states[source_node] = self.Node(
                        name = source_node,
                        next_states = set([transition[4]]),
                        edges = [{
                            'read': transition[1],
                            'write': transition[2],
                            'move': transition[3],
                            'destination_node': transition[4],
                            }],
                        )
                else:
                    self.states[source_node].next_states.add(transition[4])
                    edge = {
                            'read': transition[1],
                            'write': transition[2],
                            'move': transition[3],
                            'destination_node': transition[4],
                            }
                    if edge not in self.states[source_node].edges:
                        self.states[source_node].edges.append(edge)

            TTABLE.close()

    def input_is_valid(self):
        for item in list(self.input_string):
            if item not in self.alphabet:
                print(f'{item} not available in Σ')
                self.halt()
        return True

    def check_integrity_of_edges(self, edges):
        r = [edge['read'] for edge in edges]
        w = [edge['write'] for edge in edges]
        m = [edge['move'] for edge in edges]
        
        for item in r:
            if item not in self.gamma:
                print(f'{item} (read char) not available in Γ')
                self.halt()
        for item in w:
            if item not in self.gamma:
                print(f'{item} (read char) not available in Γ')
                self.halt()
        for item in m:
            if item not in self.allowed_moves:
                print(f'{item} not available in move set of tape')
                self.halt()
        return len(r) == len(set(r))

    def halt(self):
        if self.current_state == self.final_state:
            print('Input is accepted')
        else:
            print('Input is rejected')
        print(f'current state: {self.current_state}')
        if self.step_counter == tolerance: print('Maximum Limit Of Steps Reached')
        else: print(f'Total Steps: {self.step_counter}')
        exit()
        
    def apply_move(self, move):
        match move:
            case 'R':
                return 1
            case 'L':
                return -1
            case _:
                return 0

    def process_input(self):
        if self.input_string:
            checked_nodes = set()
            while (self.current_state != self.final_state) and (self.step_counter < tolerance):
                edges = self.current_state.edges
                head = self.head
                matched = False
                visualize_tape(data_list=self.tape, head_index=self.head, window_size=5, speed=speed)
                if self.current_state not in checked_nodes:
                    if self.check_integrity_of_edges(edges):
                        checked_nodes.add(self.current_state)
                        for edge in edges:
                            self.step_counter += 1
                            if self.tape[head] == edge['read']:
                                matched = True
                                self.tape[head] = edge['write']
                                self.head += self.apply_move(edge['move'])
                                self.current_state = self.states[edge['destination_node']]
                                break
                        if not matched:
                            self.halt()
                    else:
                        print(f'Invalid edges on {self.current_state}')
                        self.halt()
                else:
                    for edge in edges:
                        self.step_counter += 1
                        if self.tape[head] == edge['read']:
                            matched = True
                            self.tape[head] = edge['write']
                            self.head += self.apply_move(edge['move'])
                            self.current_state = self.states[edge['destination_node']]
                            break
                    if not matched:
                        self.halt()
            self.halt()  

    def __str__(self):
        return self.name

class Stay_Turing(Turing):
    def __init__(self):
        super().__init__()
        self.allowed_moves = ['R', 'L', 'S']

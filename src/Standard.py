import csv
from time import sleep
from src.Terminal import Colors
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
     
    def __init__(self, speed, tolerance):
        self.name = 'default'
        self.input_string = ''
        self.alphabet = []
        self.gamma = []
        self.tape = Tape()
        self.allowed_moves = ['R', 'L']
        self.states = dict()
        self.start_state = self.Node()
        self.final_state = None
        self.step_counter = 0
        self.tolerance = tolerance
        self.speed = speed
        self.type = 'STD'

    def get_machine_type(self):
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                if i == 1:
                    if len(line) > 2 and line[2].strip():
                        self.type = line[2].strip()
                    else:
                        self.type = 'STD'

    def fetch_data(self):
        with open('data.csv', 'r') as DATA:
            reader = csv.reader(DATA)
            for line in reader:
                if reader.line_num == 1:
                    self.name = line[0]
                    self.input_string = line[1]
                    for char in self.input_string:
                        self.tape.write(char)
                        self.tape.move_right()
                    self.tape.position = 0
                    self.alphabet = list(line[2].split('-'))
                    self.gamma = list(line[3].split('-'))
                
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

    def halt(self):
        if self.current_state == self.final_state:
            print('Input is accepted')
        else:
            print('Input is rejected')
        print(f'current state: {self.current_state}')
        if self.step_counter == self.tolerance: print('Maximum Limit Of Steps Reached')
        else: print(f'Total Steps: {self.step_counter}')
        exit()

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
                print(f'{item} (read char) is not available in Γ')
                self.halt()
        for item in w:
            if item not in self.gamma:
                print(f'{item} (write char) is not available in Γ')
                self.halt()
        for item in m:
            if item not in self.allowed_moves:
                print(f'{item} is not available in move set of tape')
                self.halt()
        return len(r) == len(set(r))
        
    def apply_move(self, move):
        match move:
            case 'R':
                self.tape.move_right()
            case 'L':
                return self.tape.move_left()
            case _:
                return
            
    def apply_transition(self, edges, matched):
        for edge in edges:
            if self.tape.read() == edge['read']:
                self.step_counter += 1
                matched = True
                self.tape.write(edge['write'])
                self.apply_move(edge['move'])
                self.current_state = self.states[edge['destination_node']]
                break
        if not matched:
            self.halt()
            
    def visualize_tape(self, speed=0.7):
        print(self.tape)
        sleep(speed)

    def process_input(self):
        if self.input_string:
            checked_nodes = set()
            while (self.current_state != self.final_state) and (self.step_counter < self.tolerance):
                edges = self.current_state.edges
                matched = False
                self.visualize_tape(speed=self.speed)
                if self.current_state not in checked_nodes:
                    if self.check_integrity_of_edges(edges):
                        checked_nodes.add(self.current_state)
                        self.apply_transition(edges, matched)
                    else:
                        print(f'Invalid edges on {self.current_state}')
                        self.halt()
                else:
                    self.apply_transition(edges, matched)
            self.halt()  

    def __str__(self):
        return self.name

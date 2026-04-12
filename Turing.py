import csv
from time import sleep

class Colors:
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

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
     
    def __init__(self, tape_size, speed, tolerance):
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
        self.tape_size = tape_size
        self.tolerance = tolerance
        self.speed = speed

    def fetch_data(self):
        with open('data.csv', 'r') as DATA:
            reader = csv.reader(DATA)
            for line in reader:
                if reader.line_num == 1:
                    self.name = line[0]
                    self.input_string = line[1]
                    self.tape = list(line[1])
                    self.tape.extend(['∅' for _ in range(self.tape_size - len(line[1]))])
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

    def halt(self):
        if self.current_state == self.final_state:
            print('Input is accepted')
        else:
            print('Input is rejected')
        print(f'current state: {self.current_state}')
        if self.step_counter == self.tolerance: print('Maximum Limit Of Steps Reached')
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
            
    def apply_transition(self, edges, head, matched):
        for edge in edges:
            if self.tape[head] == edge['read']:
                self.step_counter += 1
                matched = True
                self.tape[head] = edge['write']
                self.head += self.apply_move(edge['move'])
                self.current_state = self.states[edge['destination_node']]
                break
        if not matched:
            self.halt()
            
    def visualize_tape(
        self,
        data_list,
        head_index,
        window_size=5,
        speed=0.7,
        tape_color=Colors.CYAN,
        head_color=Colors.YELLOW,
        head_centered = True,
    ):
        if not data_list:
            print(f"{Colors.YELLOW}The list is empty!{Colors.RESET}")
            return

        num_elements = len(data_list)
        normalized_head_index = head_index % num_elements
        if normalized_head_index < 0:
            normalized_head_index += num_elements

        visible_elements = []
        total_window_length = (2 * window_size) + 1

        if head_centered:
            for i in range(total_window_length):
                current_offset = i - window_size
                actual_data_index = (normalized_head_index + current_offset) % num_elements
                visible_elements.append(data_list[actual_data_index])
            
            local_head_index = window_size
        else:
            for i in range(total_window_length):
                actual_data_index = (normalized_head_index + i) % num_elements
                visible_elements.append(data_list[actual_data_index])
            local_head_index = 0

        total_segment_width = len(visible_elements) * 5 + 1
        print(f"{tape_color}╭{'─' * total_segment_width}╮{Colors.RESET}")

        tape_line = f"{tape_color}│"
        pointer_line = " "

        for i, item in enumerate(visible_elements):
            formatted_item = str(item).center(3)
            block_width = 5

            if i == local_head_index:
                tape_line += f"{tape_color}{head_color}{Colors.BOLD} {formatted_item} {Colors.RESET}{tape_color}"
                pointer_line += f"{' ' * ((block_width - 1) // 2)}{head_color}▲{Colors.RESET}{' ' * ((block_width - 1) // 2)}"
            else:
                tape_line += f"{tape_color} {formatted_item} "
                pointer_line += " " * block_width
                
        tape_line += f"│{Colors.RESET}"
        print(tape_line)
        print(f"{tape_color}╰{'─' * total_segment_width}╯{Colors.RESET}")
        print(pointer_line)
        print(f"{Colors.BOLD}{Colors.WHITE}----------------------------------------{Colors.RESET}")
        print(f"Current Head: {head_color}{Colors.BOLD}{data_list[normalized_head_index]}{Colors.RESET} at index {normalized_head_index}\n")
        sleep(speed)

    def process_input(self):
        if self.input_string:
            checked_nodes = set()
            while (self.current_state != self.final_state) and (self.step_counter < self.tolerance):
                edges = self.current_state.edges
                head = self.head
                matched = False
                self.visualize_tape(data_list=self.tape, head_index=self.head, window_size=5, speed=self.speed)
                if self.current_state not in checked_nodes:
                    if self.check_integrity_of_edges(edges):
                        checked_nodes.add(self.current_state)
                        self.apply_transition(edges, head, matched)
                    else:
                        print(f'Invalid edges on {self.current_state}')
                        self.halt()
                else:
                    self.apply_transition(edges, head, matched)
            self.halt()  

    def __str__(self):
        return self.name

class Stay_Turing(Turing):
    def __init__(self, tape_size, speed, tolerance):
        super().__init__(tape_size, speed, tolerance)
        self.allowed_moves.append('S')

class Semi_Infinite_Turing(Turing):
    def __init__(self, tape_size, speed, tolerance):
        super().__init__(tape_size, speed, tolerance)
    
    def apply_move(self, move):
        match move:
            case 'R':
                return 1
            case 'L':
                if self.head <= 0:
                    return 0
                return -1
            case _:
                return 0
            
    def visualize_tape(
            self,
            data_list,
            head_index,
            window_size=5,
            speed=0.7,
            tape_color=Colors.CYAN,
            head_color=Colors.YELLOW,
            head_centered = False,
    ):
        return super().visualize_tape(data_list, head_index, window_size, speed, tape_color, head_color, head_centered)

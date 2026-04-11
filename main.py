from Turing import *

if __name__ == '___main__':
    machine = Turing()
    machine.fetch_data()
    machine.fetch_transitions()
    print(machine.name)
    print(f'Σ: {machine.alphabet}')
    print(f'Γ: {machine.gamma}')
    machine.input_is_valid()
    print(f'Input: {machine.input_string}')
    machine.process_input()

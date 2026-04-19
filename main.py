from src.Standard import Turing

if __name__ == '__main__':
    tolerance = int(input('Enter Maximum Steps of Machine: '))
    speed = float(input('Enter Speed Of Visualization Of Tape (Recommended = 0.7s): '))
    machine = Turing(tolerance=tolerance, speed=speed)
    machine.fetch_data()
    machine.fetch_transitions()
    print(machine.name)
    print(f'Σ: {machine.alphabet}')
    print(f'Γ: {machine.gamma}')
    machine.input_is_valid()
    print(f'Input: {machine.input_string}')
    machine.process_input()

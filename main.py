from src.Standard import Turing
from src.Semi_Infinite import Semi_Infinite_Turing
from src.Stay import Stay_Turing
from src.Multi_Tape import Multi_Tape_Turing
from src.Offline import Offline_Turing
from src.Multi_Dimension import Multi_Dimension_Turing

MACHINE_TYPES = {
    'STD':   Turing,
    'SINF':  Semi_Infinite_Turing,
    'STAY':  Stay_Turing,
    'OFFL':  Offline_Turing,
    'MTAPE': Multi_Tape_Turing,
    'MDIM':  Multi_Dimension_Turing,
}

if __name__ == '__main__':
    tolerance = int(input('Enter Maximum Steps of Machine: '))
    speed = float(input('Enter Speed Of Visualization Of Tape (Recommended = 0.7s): '))
    m = Turing(tolerance=tolerance, speed=speed)
    m.get_machine_type()
    machine_class = MACHINE_TYPES.get(m.type, Turing)
    machine = machine_class(tolerance=tolerance, speed=speed)
    machine.fetch_data()
    machine.fetch_transitions()
    print(machine.name)
    print(f'Machine Type: {machine.type}')
    print(f'Σ: {machine.alphabet}')
    print(f'Γ: {machine.gamma}')
    machine.input_is_valid()
    print(f'Input: {machine.input_string}')
    machine.process_input()


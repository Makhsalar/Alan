from src.Standard import Turing
from src.Semi_Infinite import Semi_Infinite_Turing
from src.Stay import Stay_Turing
from src.Multi_Tape import Multi_Tape_Turing
from src.Offline import Offline_Turing
from src.Multi_Dimension import Multi_Dimension_Turing
from src.Non_Deterministic import Non_Deterministic_Turing

MACHINE_TYPES = {
    'STD':   Turing,
    'SINF':  Semi_Infinite_Turing,
    'STAY':  Stay_Turing,
    'OFFL':  Offline_Turing,
    'MTAPE': Multi_Tape_Turing,
    'MDIM':  Multi_Dimension_Turing,
    'NON':   Non_Deterministic_Turing,
}

if __name__ == '__main__':
    machine_class = Turing().get_machine_type() 
    machine_class = MACHINE_TYPES.get(machine_class, Turing)
    tolerance = int(input('Enter Maximum Steps of Machine: '))
    machine = machine_class(tolerance=tolerance)
    machine.run()

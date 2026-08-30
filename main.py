from src.Multi_Tape import Multi_Tape_Stay_Turing, Multi_Tape_Turing
from src.Multi_Track import Multi_Track_Turing
from src.Semi_Infinite import Semi_Infinite_Turing
from src.Standard import Turing
from src.Stay import Stay_Turing

MACHINE_TYPES = {
    "STD": Turing,
    "STAY": Stay_Turing,
    "SINF": Semi_Infinite_Turing,
    "MTAPE": Multi_Tape_Turing,
    "SMTAPE": Multi_Tape_Stay_Turing,
    "MTRK": Multi_Track_Turing,
}

if __name__ == "__main__":
    machine_type = Turing().get_machine_type()
    machine_class = MACHINE_TYPES.get(machine_type, Turing)
    tolerance = int(input("Enter Maximum Steps of Machine: "))
    match machine_type:
        case "MTAPE" | "SMTAPE" | "MTRK":
            number_of_tapes = int(input("Enter Number of Tapes/Tracks: "))
            machine = machine_class(tolerance=tolerance, num_tape=number_of_tapes)
            machine.run()
        case _:
            machine = machine_class(tolerance=tolerance, num_tape=1)
            machine.run()

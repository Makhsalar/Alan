# Alan — Multi-Type Turing Machine Simulator

A Python simulator for various Turing machine variants with CSV-based machine definitions.

## Features

- **6 Machine Types**: Standard, Stay, Semi-Infinite, Multi-Tape, Multi-Tape Stay, Multi-Track
- **CSV Configuration**: Define machines via simple CSV files
- **Step Visualization**: Optional tape state visualization per step
- **Type-Safe**: Full type annotations, passes `pyright` and `ruff`

## Machine Types

| Code     | Type            | Description                                          |
| -------- | --------------- | ---------------------------------------------------- |
| `STD`    | Standard        | Classic Turing machine (bidirectional infinite tape) |
| `STAY`   | Stay            | Standard + `S` (stay) move                           |
| `SINF`   | Semi-Infinite   | Tape bounded on left (position ≥ 0)                  |
| `MTAPE`  | Multi-Tape      | Multiple independent tapes                           |
| `SMTAPE` | Multi-Tape Stay | Multi-tape + `S` move                                |
| `MTRK`   | Multi-Track     | Single tape, multiple tracks (shared head)           |

## Installation

```bash
Pure Python
```

## Quick Start

```bash
# Run with default machine (data.csv + transitions.csv in project root)
python main.py

# Or run a specific machine from ./Machines/
cp Machines/IsEven-SMTAPE/data.csv .
cp Machines/IsEven-SMTAPE/transitions.csv .
python main.py
```

Input prompt:

```
Enter Maximum Steps of Machine: 10000
Enter Number of Tapes/Tracks: 2    # Only for MTAPE/SMTAPE/MTRK
```

## CSV Format

### `data.csv` — Machine Definition

Two-row format:

```csv
name,input_tape0,input_tape1,...,Σ0,Σ1,...,Γ0,Γ1,...
start_state,final_state,machine_type
```

**Example** (`Machines/IsEven-SMTAPE/data.csv`):

```csv
IsEven,1111,1,1-_,1,1,1-0
q0,qf,SMTAPE
```

| Column         | Description                                              |
| -------------- | -------------------------------------------------------- |
| `name`         | Machine identifier                                       |
| `input_tapeN`  | Initial tape content for tape N                          |
| `ΣN`           | Alphabet (no blank), `-` separated                       |
| `ΓN`           | Tape alphabet (with blank `_`), `-` separated            |
| `start_state`  | Initial state name                                       |
| `final_state`  | Accepting/halt state                                     |
| `machine_type` | One of: `STD`, `STAY`, `SINF`, `MTAPE`, `SMTAPE`, `MTRK` |

### `transitions.csv` — Transition Table

Format varies by machine type:

**Standard / Stay / Semi-Infinite / Multi-Tape / Multi-Tape Stay:**

```csv
source,read0,write0,move0,read1,write1,move1,...,destination
```

**Multi-Track (shared head):**

```csv
source,read0,write0,read1,write1,...,move,destination
```

**Example** (`Machines/IsEven-SMTAPE/transitions.csv`):

```csv
q0,1,1,R,1,0,S,q1
q0,_,_,S,1,1,S,qf
q1,1,1,R,0,1,S,q0
q1,_,_,S,0,0,S,qf
```

Columns per tape: `read`, `write`, `move` (except MTRK: single `move` at end).

## Project Structure

```
Alan/
├── main.py                 # Entry point
├── data.csv                # Active machine definition
├── transitions.csv         # Active transition table
├── src/
│   ├── Standard.py         # Base Turing machine
│   ├── Tape.py             # Tape implementation
│   ├── Stay.py             # Stay variant
│   ├── Semi_Infinite.py    # Semi-infinite variant
│   ├── Multi_Tape.py       # Multi-tape variants
│   └── Multi_Track.py      # Multi-track variant
└── Machines/               # Pre-built examples
    ├── aⁿbⁿcⁿ; n≥1-STD/
    ├── Binary_Addition-STD/
    ├── Binary_Addition_Multi_Same_len-MTAPE/
    ├── Factorial-SMTAPE/
    ├── IsEven-SMTAPE/
    └── Reverse-SMTAPE/
```

## Example Machines

| Machine                 | Type   | Description                      |
| ----------------------- | ------ | -------------------------------- |
| `aⁿbⁿcⁿ`                | STD    | Accepts equal numbers of a, b, c |
| `Binary_Addition`       | STD    | Adds two binary numbers          |
| `Binary_Addition_Multi` | MTAPE  | Multi-tape binary addition       |
| `Factorial`             | SMTAPE | Computes factorial               |
| `IsEven`                | SMTAPE | Checks if unary input is even    |
| `Reverse`               | SMTAPE | Reverses tape content            |

## Notes

- The simulator reads `data.csv` and `transitions.csv` from the **current working directory**
- To test a machine from `Machines/`, copy its CSV files to the project root
- `SMTAPE` and `MTRK` require `num_tapes` > 1 at runtime
- Visualization prompts after execution completes (press `y` + Enter, then enter speed)

## License

MIT

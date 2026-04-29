# Instructions for Adding Turing Machine Data

You must add **your transitions** and **machine data** into the provided `.csv` files.  
Use the `sample.csv` files as templates — **your data must follow the exact same structure and column patterns**.

There are already **two Turing machines** available in the `./Machines` directory.  
The project will automatically process **all** Turing machines placed in that folder.

---

## File Requirements

### 1. Data File (`data.csv`)
This file stores general machine information.

#### **Columns (follow sample.csv exactly):**
- `name` — The machine’s name  
- `input_string` — The input given to the machine  
- `a-b` — Machine’s alphabet without blank  
- `a-b-_` — Machine’s alphabet including blank  
- `start_state` — Initial state  
- `final_state` — Accepting/halting state  

**Sample structure:**
```
name,input_string,Σ,Γ
start_state,final_state
```

---

### 2. Transition File (`transition.csv`)
This file defines the machine’s state transitions.

#### **Columns (follow sample.csv exactly):**
- `source_node` — Current state  
- `read` — Symbol read from tape  
- `write` — Symbol written to tape  
- `move` — Head direction (`L`, `R`, or `S`)  
- `destination_node` — Next state  

**Sample structure:**
```
source_node,read,write,move,destination_node
```

---

## Summary
1. Add your machine definitions into the CSV files.  
2. Follow the *exact* sample patterns — column order, spelling, and structure.  
3. Place your machine folders inside `./Machines`.
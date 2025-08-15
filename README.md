# Line-Covering: Two Drones (MinMax Criterion)

This module implements and compares algorithms for **covering line segments with two drones** under the **MinMax criterion** — minimizing the maximum tour length of any drone.  
It evaluates:

1. **G2D** — Greedy 2-Drones algorithm.
2. **G2D-CutEnlarge** — Greedy with cutting and enlarging adjustments.
3. **MILP formulation** solved using Gurobi.
4. **Dynamic Programming MinSum** — initial tour construction method.

The goal is to compare approximated and exact approaches on randomly generated line segment configurations.

## Algorithms Overview

### 1. Dynamic Programming MinSum
Constructs tours that minimize the **sum** of tour lengths.  
This serves as the starting solution for subsequent heuristic algorithms.

### 2. Greedy 2-Drones
Splits the constructed tours between two drones in a **greedy manner**  
to minimize the **maximum** tour length (load) assigned to any drone.

### 3. Cut and Enlarge
Refines the greedy solution by:
- Cutting overly long tours
- Enlarging shorter ones  
This re-balancing aims to further reduce the maximum load difference between drones.

### 4. MILP Solver
Formulates the problem as a **Mixed-Integer Linear Program**  
and solves it optimally using **Gurobi**.

---

## License
This project is distributed under the repository's main license  
(see the root of the repository for details).

---

## Author
This code was developed by **Alina Kasiuk**. 
As a part of the research **Covering line segments with drones: the minmax criterion**. 
Authors: **José Miguel Díaz-Bañez, José Manuel Higes, Alina Kasiuk and Inmaculada Ventura**. 
Part of the **ETSI GALGO** research codebase.


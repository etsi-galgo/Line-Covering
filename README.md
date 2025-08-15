# Line-Covering: Two Drones (MinMax Criterion)

This module implements and compares algorithms for **covering line segments with two drones** under the **MinMax criterion** — minimizing the maximum tour length of any drone.  
It evaluates:

1. **G2D** — Greedy 2-Drones algorithm.
2. **G2D-CutEnlarge** — Greedy with cutting and enlarging adjustments.
3. **MILP formulation** solved using Gurobi.
4. **Dynamic Programming MinSum** — initial tour construction method.

The goal is to compare approximated and exact approaches on randomly generated line segment configurations.

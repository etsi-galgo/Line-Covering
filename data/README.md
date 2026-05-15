# Dataset Description

This folder contains the datasets used in the experimental evaluation of the algorithms presented in the paper "Optimizing Line Segment Inspection with Limited-Range Drones".

---

## Experiment 1: Influence of Segment Homogeneity and Maximum Tour Length

In the first experiment, we investigate how the segment homogeneity and the maximum tour length \(L\) influence the approximation factor of the algorithms.

A total of **987 scenarios** were generated with:

- \(m = -1000\)
- \(M = 1000\)
- \(d = 1000\)

Although individual segments may lie anywhere within \([-1000,1000]\), the maximum distance between the leftmost and rightmost endpoints of any two segments is constrained to 1000.

The parameters were generated as follows:

- \(L\) randomly selected in \([L_{min}, L_{max}]\)
- \(X_b \in [0,1000]\)
- \(Y_b \in [1,10000]\)

Segment homogeneity is measured using the coefficient of variation (CV) of the segment lengths.

Three homogeneity levels were considered:

| Homogeneity Level | Target CV | Number of Cases |
|---|---|---|
| High Homogeneity | 0.2 | 429 |
| Medium Homogeneity | 0.6 | 278 |
| Low Homogeneity | 0.8 | 280 |

The segment length distribution was generated with a fixed mean value of 10.

---

### Evaluated Metrics

Two approximation factors are evaluated:

- \(\Delta\): approximation factor of algorithm G2D
- \(\Delta_I\): approximation factor of the improved algorithm

If \(T_2\) is the solution obtained by one of the proposed algorithms and \(T_2^*\) is the optimal solution obtained using Gurobi, the approximation factor is defined as:

\[
\frac{\ell(T_2)}{\ell(T_2^*)}
\]

---

### File Description

### `experiment_1.csv`

| Column | Description |
|---|---|
| `Hom` | Target segment homogeneity level. `0`: 20%, `1`: 80% |
| `medLongSeg` | Target mean segment length |
| `CV` | Real coefficient of variation of segment lengths |
| `nSeg` | Target density. `0`: 20%, `1`: 80% |
| `nSegNum` | Number of segments |
| `Base` | Maximum tour length category |
| `BaseNum` | Real maximum tour length value |
| `L` | Maximum allowed tour length category |
| `Lprop` | Relative maximum tour length proportion |
| `gurobiMinMax` | Optimal MinMax solution obtained with Gurobi |
| `gurobiT1` | Number of tours assigned to drone 1 in the Gurobi solution |
| `gurobiT2` | Number of tours assigned to drone 2 in the Gurobi solution |
| `greedyMinMax` | MinMax solution obtained with the greedy algorithm |
| `greedyT1` | Number of tours assigned to drone 1 in the greedy solution |
| `greedyT2` | Number of tours assigned to drone 2 in the greedy solution |
| `improvedMinMax` | MinMax solution obtained with the improved greedy algorithm |
| `improvedT1` | Number of tours assigned to drone 1 in the improved solution |
| `improvedT2` | Number of tours assigned to drone 2 in the improved solution |
| `errorGreedyAbs` | Absolute error of the greedy solution |
| `errorGreedy` | Relative error of the greedy solution: `(greedyMinMax - gurobiMinMax)/gurobiMinMax` |
| `errorImprovedAbs` | Absolute error of the improved solution |
| `errorImproved` | Relative error of the improved solution: `(improvedMinMax - gurobiMinMax)/gurobiMinMax` |
| `kGreedy` | Approximation factor of the greedy algorithm |
| `kImproved` | Approximation factor of the improved algorithm |

---

# Reproducibility

The experiments can be reproduced using the source code available in the repository:

https://github.com/etsi-galgo/Line-Covering

---

# License

This dataset is provided for academic and research purposes.

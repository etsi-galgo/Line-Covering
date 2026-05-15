# Dataset Description

This folder contains the datasets used in the experimental evaluation of the algorithms presented in the paper "Optimizing Line Segment Inspection with Limited-Range Drones".

---

## Experiment 1: Influence of Segment Homogeneity and Maximum Tour Length

In the first experiment, we investigate how the segment length homogeneity and the maximum tour length \(L\) influence the approximation factor of the algorithms.

A total of **987 scenarios** were generated.

---

### File Description

### `experiment_1.csv`

| Column | Description |
|---|---|
| `Hom` | Segment length homogeneity. `0`: 20%, `1`: 60-80% |
| `medLongSeg` | Mean segment length |
| `CV` | Coefficient of variation of segment lengths |
| `nSeg` | Segments density (Portion of line corresponding to a segment). `0`: 20%, `1`: 80% |
| `nSegNum` | Number of segments |
| `Base` | Base location height ($Y_b$). `0`: $Y_b<1$, `1`: $Y_b>1$ |
| `BaseNum` | Base location height ($Y_b$ value) |
| `L` | Maximum allowed tour length. `0`: $0<L^*<0.5$, `1`: $0.5<L^*<1$ |
| `Lprop` | Normalized maximum allowed tour length ($L^* = L/L_max$)|
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

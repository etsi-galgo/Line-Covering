# Dataset Description

This folder contains the datasets used in the experimental evaluation of the algorithms presented in the paper "Optimizing Line Segment Inspection with Limited-Range Drones".

---

## Experiment 1

In the first experiment, we investigate how the segment length homogeneity and the maximum tour length \(L\) influence the approximation factor of the algorithms.

A total of **987 scenarios** were generated.

---

### File Description

### `experiment_1.csv`

| Column | Description |
|---|---|
| `Hom` | Segment length homogeneity. `0`: CV = 20%, `1`: CV = 60...80% |
| `medLongSeg` | Mean segment length |
| `CV` | Coefficient of variation of segment lengths |
| `nSeg` | Number of segments. `0`: SegNum < 40, `1`: SegNum > 40 |
| `nSegNum` | Number of segments (int value)|
| `Base` | Base location height ($Y_b$). `0`: $Y_b<1$, `1`: $Y_b>1$ |
| `BaseNum` | Base location height ($Y_b$ value) |
| `L` | Maximum allowed tour length. `0`: $0<L^\*<0.5$, `1`: $0.5<L^\*<1$ |
| `Lprop` | Normalized maximum allowed tour length ($L^\* = L/L_{max}$)|
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

# Experiment 2

In the second experiment, we extend the analysis by incorporating the segment density as an additional experimental factor.

A total of **3306 scenarios** were generated 

In this experiment, the discretization level \(d\) was reduced compared to previous experiments in order to mitigate the computational limitations of the Gurobi solver, as reflected in the execution times reported later.

To systematically evaluate the influence of the maximum tour length \(L\), the base station was fixed.


### File Description

### `experiment_2.csv`

| Column | Description |
|---|---|
| `nSeg` | Number of segments. `0`: SegNum < 40, `1`: SegNum > 40 |
| `nSegNum` | Number of segments (int value) |
| `CV` | Target coefficient of variation of segment length: `0`: targetCV = 20%, `1`: targetCV = 80% |
| `realCV` | Real coefficient of variation of segment lengths |
| `targetMean` | Target mean segment length |
| `realMean` | Real mean segment length |
| `Density` | Target density of segments:  `0`: targetDensity = 20%, `1`: targetDensity = 80%|
| `realDensity` | Real segment density |
| `L` | Maximum allowed tour length. `0`: $L < L_{min}+29,8$, `1`:  $L < L_{min}+241$, `2`:  $L < L_{max}$ |
| `numL` | Real maximum allowed tour length |
| `gurobiMinMax` | Optimal MinMax solution obtained with Gurobi |
| `greedyMinMax` | MinMax solution obtained with the greedy algorithm |
| `greedyT1` | Number of tours assigned to drone 1 in the greedy solution |
| `greedyT2` | Number of tours assigned to drone 2 in the greedy solution |
| `improvedMinMax` | MinMax solution obtained with the improved greedy algorithm |
| `improvedT1` | Number of tours assigned to drone 1 in the improved solution |
| `improvedT2` | Number of tours assigned to drone 2 in the improved solution |
| `errorGreedyAbs` | Absolute error of the greedy solution |
| `errorGreedy` | Relative error of the greedy solution |
| `errorImprovedAbs` | Absolute error of the improved solution |
| `errorImproved` | Relative error of the improved solution |
| `kGreedy` | Approximation factor of the greedy algorithm |
| `kImproved` | Approximation factor of the improved algorithm |
| `timeGreedy` | Execution time of the greedy algorithm (seconds) |
| `timeImproved` | Execution time of the improved greedy algorithm (seconds) |
| `timeGurobi` | Execution time of the Gurobi solver (seconds) |


# Reproducibility

The experiments can be reproduced using the source code available in the repository:

https://github.com/etsi-galgo/Line-Covering

---

# License

This dataset is provided for academic and research purposes.

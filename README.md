# Wipro 5G Capstone Project

## 5G MAC Scheduler Comparison

## Problem Statement

In a 5G downlink cell, the base station must decide which User Equipment (UE) receives radio resources in each scheduling interval. This decision affects total cell throughput, fairness among users, and service quality for UEs at the cell edge. A scheduler designed only for high throughput can repeatedly favour UEs with better channels, while an overly fair scheduler may reduce spectral efficiency.

This project compares Round-Robin (RR), Proportional Fair (PF), and Maximum Carrier-to-Interference (Max-C/I) scheduling under time-varying wireless channel conditions.

## Objectives

- Develop a Python-based 5G downlink MAC scheduler simulator.
- Model multiple UEs with different average channel conditions and slot-level fading.
- Implement Round-Robin, Proportional Fair, and Max-C/I schedulers.
- Measure cell throughput, Jain's fairness index, and cell-edge throughput.
- Present reproducible output through a CSV summary and comparison chart.

## Technology Stack

| Area | Technology |
|---|---|
| Programming language | Python 3.10+ |
| Numerical simulation | NumPy |
| Result processing | Pandas |
| Visualisation | Matplotlib |

## Project Structure

```text
wipro-5g-mac-scheduler-comparison/
├── src/
│   └── mac_scheduler_simulator.py
├── results/                         # Generated at runtime
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Implementation Steps

1. Defined a multi-UE downlink scenario with UEs distributed from near-cell to cell-edge locations.
2. Applied distance-based large-scale channel gain and slot-wise Rayleigh fading.
3. Converted the resulting SNR to a capped Shannon-style spectral efficiency.
4. Implemented RR, PF, and Max-C/I selection rules.
5. Accumulated per-UE delivered data across 1 ms scheduling slots.
6. Calculated cell throughput, Jain's fairness index, and mean throughput for the lowest-channel-quality 20% of UEs.
7. Exported a CSV metrics table and a PNG comparison chart.

## Scheduling Algorithms

| Scheduler | Selection rule | Expected behaviour |
|---|---|---|
| Round-Robin | Selects UEs in a fixed cyclic order | Strong access fairness, channel quality is not considered |
| Proportional Fair | Maximises instantaneous rate divided by past average rate | Balances throughput and fairness |
| Max-C/I | Selects the UE with the best instantaneous rate | High cell throughput; cell-edge users may receive less service |

## Setup and Execution

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
python src/mac_scheduler_simulator.py
```

For a smaller trial run:

```bash
python src/mac_scheduler_simulator.py --users 10 --slots 1000
```

## Output

The program creates the following files in `results/`:

- `scheduler_metrics.csv` — metric values for all schedulers.
- `scheduler_comparison.png` — side-by-side comparison of throughput, fairness, and cell-edge throughput.

The command window also displays a formatted metrics table. Exact values may change when the seed, UE count, or number of slots is changed.

## Evaluation Criteria

| Metric | Purpose |
|---|---|
| Cell Throughput (Mbps) | Total rate delivered by the cell across all UEs |
| Jain Fairness Index | Equality of throughput allocation; 1.0 indicates perfect equality |
| Cell-Edge Throughput (Mbps) | Average throughput of the farthest 20% of UEs |

## Deliverables Implemented

- Python source program implementing three scheduling algorithms.
- Reproducible dependency list.
- CSV and chart generation for measured output.
- Technical project documentation with setup, execution, metrics, and references.

## References

1. A. Goldsmith, *Wireless Communications*, Cambridge University Press, 2005.
2. M. Andrews, K. Kumaran, K. Ramanan, A. Stolyar, P. Whiting, and R. Vijayakumar, “Providing Quality of Service over a Shared Wireless Link,” *IEEE Communications Magazine*, 2001.
3. 3GPP TS 38.300, *NR; NR and NG-RAN Overall Description*, 3rd Generation Partnership Project.
4. 3GPP TS 38.214, *NR; Physical Layer Procedures for Data*, 3rd Generation Partnership Project.
5. R. Jain, D.-M. Chiu, and W. Hawe, *A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems*, DEC Research Report TR-301, 1984.


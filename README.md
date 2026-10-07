# CPU Scheduling Algorithm Simulator

A modern, desktop application built in Python 3 using Tkinter and Matplotlib for visualizing, simulating, and comparing key Operating System (OS) CPU scheduling algorithms.

---

## Features

- **Supported Algorithms**:
  1. **First-Come, First-Served (FCFS)**: Non-preemptive scheduling based strictly on arrival order.
  2. **Shortest Job First (SJF)**: Non-preemptive scheduling prioritizing processes with the shortest burst time.
  3. **Priority Scheduling**: Non-preemptive scheduling where lower priority numbers represent higher priority.
  4. **Round Robin (RR)**: Preemptive scheduling using a custom Time Quantum and ready queue.

- **Key Functionality**:
  - **Dynamic Gantt Chart**: Embedded Matplotlib visualization showing execution timelines, preemptions, and CPU IDLE states.
  - **Metrics Computation**: Calculates Completion Time (CT), Turnaround Time (TAT = CT - AT), Waiting Time (WT = TAT - BT), and overall averages.
  - **Algorithm Comparison**: "Run All & Compare" mode runs all four algorithms using the exact same process dataset.
  - **Robust Input Validation**: Prevents application crashes by catching empty fields, duplicate Process IDs, negative arrival times, zero/negative burst times, and invalid time quanta.
  - **Modern UI**: Polished Black and Beige dark-themed dashboard.

---

## Project Structure

```text
cpu_scheduling_simulator/
├── main.py
├── calculations.py
├── visualization.py
├── requirements.txt
├── README.md
├── algorithms/
│   ├── __init__.py
│   ├── fcfs.py
│   ├── sjf.py
│   ├── priority.py
│   └── round_robin.py
└── gui/
    ├── __init__.py
    └── simulator_gui.py
```

## Project Links

- **GitHub Repository:** [View Repository](https://github.com/Ardra-Sobharaj/cpu-scheduling-algorithm-simulator)
- **Download / Deployment:** [Download Simulator](https://github.com/Ardra-Sobharaj/cpu-scheduling-algorithm-simulator/releases/latest)

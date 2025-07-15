# OR Simulation Competition

### Project Summary

For the IISE-SHS Student Simulation Competition, our team developed a system to find the most "ethical and effective" configuration for a surgical center. By optimizing both case scheduling and nurse staffing levels, our final model achieved a **26% improvement in OR utilization** while maintaining **zero median staff overtime**. This work was recognized with multiple awards, including 3rd place in the IISE regional technical paper competition, and was presented at the IISE 2023 Annual Conference.

---

### Methodology & Technical Stack

* **Primary Tool:** FlexSim (Discrete-Event Simulation)
* **Core Methodologies:** Binary Search Algorithm, Heuristic Scheduling, Cost-Benefit Analysis, What-If Scenarios

Our solution was a two-phase optimization process:

1.  **Optimizing the Schedule:** To manage the variability of surgery times, we developed a scheduling algorithm that incorporated a "time buffer." We then used a **Binary Search algorithm** to efficiently find the optimal buffer size, which maximized the OR's workload while ensuring operations remained ethically feasible (i.e., no excessive overtime).

2.  **Optimizing Staff Levels:** With the optimized schedule, we ran further simulation experiments to fine-tune the number of Pre-Op, Circulation, Scrub, and PACU nurses. This cost-benefit analysis identified the minimum staffing required to maintain high performance, saving significant potential labor costs.

---

### Awards & Recognition

* Presented at the **IISE 2023 Annual Conference**
* **3rd Place:** IISE Regional Technical Paper Competition
* **2nd Place:** Engineering Research Poster Competition

---

### Project Artifacts

* `OR_Optimization_Paper.pdf`: The full academic paper detailing our methodology and findings.
* `OR_Optimization_Poster.png`: The research poster presented at the engineering research competition.
* `OR_Optimization_Presentation.pdf`: The slide deck used for the conference presentation.

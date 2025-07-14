# Operating Room Scheduling & Staffing Optimization

### Project Highlights

* **Challenge:** As part of the IISE-SHS Student Simulation Competition, our team was tasked with finding the most "ethical and effective" configuration for a surgical center. [cite_start]This involved optimizing case scheduling and nurse staffing levels to maximize operating room (OR) utilization while respecting critical ethical constraints like minimizing staff overtime. [cite: 12, 13, 228, 229, 230]
* [cite_start]**Methodology:** We developed a custom scheduling algorithm in **FlexSim** and used a **Binary Search algorithm** to systematically find the optimal "time buffer." [cite: 64, 449] This allowed us to maximize the scheduled workload while ensuring the probability of excessive staff overtime remained near zero. [cite_start]The final configuration was then fine-tuned through a cost-benefit analysis of different nurse staffing levels. [cite: 221]
* **Outcome:** Our final configuration resulted in a **26% improvement in OR utilization** with **zero median staff overtime**. [cite_start]The project was recognized with multiple awards and was presented at the IISE 2023 Annual Conference. [cite: 185]

---

### The Approach: A Two-Phase Optimization

Our solution tackled two distinct but related problems: scheduling the work and staffing the floor.

1.  **Case Scheduling via Binary Search:**
    * The core challenge in scheduling is managing variability. [cite_start]A schedule that looks perfect on average can easily run long, causing excessive overtime. [cite: 289]
    * [cite_start]We implemented a **time buffer** system, intentionally under-scheduling the total expected work to absorb delays. [cite: 218, 294]
    * [cite_start]To find the perfect buffer, we used a **Binary Search algorithm**, starting with 0% and 50% buffers and iteratively narrowing the search space. [cite: 449, 451, 452] This allowed us to efficiently find the highest possible workload that remained ethically feasible across multiple simulation runs.

2.  **Fine-Tuning Nurse Staffing:**
    * [cite_start]With an optimized schedule, we then ran experiments in FlexSim to fine-tune the number of Pre-Op, Circulation, Scrub, and PACU nurses. [cite: 221]
    * Our analysis showed that the maximum staffing level was not the most effective. [cite_start]We identified an optimal, lower staffing configuration that maintained high performance while saving significant labor costs. [cite: 527, 528, 529]

---

### Key Results & Awards

* **Performance:** Achieved a **26% improvement** in Operating Room (OR) utilization. 
* [cite_start]**Ethical Compliance:** The final solution resulted in **0 minutes of median staff overtime**. [cite: 524]
* **Awards & Recognition:**
    * [cite_start]Presented at the **IISE 2023 Annual Conference**. [cite: 185]
    * [cite_start]**3rd Place**, IISE Regional Technical Paper Competition. [cite: 185]
    * [cite_start]**2nd Place**, Engineering Research Poster Competition. [cite: 185]

---

### Files in This Directory

* `Paper__IISE regional conference UG paper competition[2902].pdf`: The full academic paper detailing our methodology and findings.
* `Poster__Optimal surgical center operations....jpg`: The research poster presented at the engineering research competition.
* `Presentation__OPTIMIZING OPERATING ROOMS UTILIZATION.pdf`: The slide deck used for the conference presentation.
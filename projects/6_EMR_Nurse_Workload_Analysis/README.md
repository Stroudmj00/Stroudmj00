# Clinical Workload Analysis (EMR Data)

### Project Highlights

* [cite_start]**Challenge:** Investigated if the workload from Electronic Medical Record (EMR) systems is uniformly distributed among ICU nurses, a key factor in nurse burnout. [cite: 1591, 1594, 1603]
* [cite_start]**Methodology:** Analyzed a massive Real-Time Measurement System (RTMS) dataset from 7 nurses over a two-week period using **R**. [cite: 1610, 1618, 1622] [cite_start]Performed a **Chi-Square Goodness of Fit test** to compare the observed EMR task frequencies of each nurse against an expected uniform distribution. [cite: 1792]
* [cite_start]**Outcome:** The analysis **statistically rejected the hypothesis of a uniform workload** (p < 0.05). [cite: 1845, 1848] This proves that individual nurses carry a significantly different EMR burden. [cite_start]This research won 3rd and 4th place in university engineering research poster competitions. [cite: 589]

---

### The Analytical Approach

1.  [cite_start]**Data Wrangling:** Processed and compiled 160 raw CSV files from the hospital's RTMS system into a master dataset using R. [cite: 555, 1622, 1646] [cite_start]The massive dataset was filtered down to focus on the frequency of specific EMR tasks ("timernames"). [cite: 558, 1632]
2.  [cite_start]**Frequency Analysis:** Calculated the interaction frequency for the top EMR tasks performed by each of the seven nurses over the study period. [cite: 1713]
3.  [cite_start]**Statistical Testing:** Used a **Chi-Square Goodness of Fit test** to formally determine if the observed differences in task frequency among nurses were statistically significant or simply due to random chance. [cite: 1792]

---

### Key Finding & Impact

* [cite_start]**The EMR workload is not equal.** The data proves that specific nurses interact with the EMR system at a significantly different rate than their peers for the most common tasks. [cite: 1755, 1920]
* This finding challenges a one-size-fits-all approach to hospital resource management. It provides a data-driven basis for **tailoring resource allocation**—such as providing upgraded computers or other infrastructure—to the specific nurses who carry the heaviest EMR burden. [cite_start]This could improve their efficiency and help mitigate task-related burnout. [cite: 1580, 1975, 1976]

---

### Files in This Directory

* `Nurse_Workload_Report.pdf`: The full academic paper detailing the statistical analysis and findings.
* `Nurse_Workload_Poster.pdf`: The research poster presented at the engineering research competitions.
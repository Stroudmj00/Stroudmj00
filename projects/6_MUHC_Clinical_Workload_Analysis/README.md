# Clinical Workload Analysis

### Project Summary

This award-winning research project investigated the distribution of Electronic Medical Record (EMR) workload among ICU nurses to explore data-driven solutions for mitigating nurse burnout. By analyzing a massive Real-Time Measurement System (RTMS) dataset, I used a **Chi-Square Goodness of Fit test** to determine if EMR task frequencies were uniform across a team of nurses.

The analysis **statistically rejected the hypothesis of a uniform workload** (p < 0.05), proving that individual nurses carry a significantly different EMR burden. This finding provides a quantitative basis for tailoring hospital resource allocation to improve efficiency and support staff well-being. This research won 3rd and 4th place in university engineering research poster competitions.

---

### Methodology & Technical Stack

* **Language & Libraries:** R (dplyr)
* **Core Methodologies:** Data Wrangling, Statistical Inference, Hypothesis Testing (Chi-Square Goodness of Fit)

The analysis followed a three-step process:

1.  **Data Wrangling:** Processed and compiled 160 raw CSV files from the hospital's RTMS system, filtering the massive dataset to focus on the frequency of specific EMR tasks.
2.  **Frequency Analysis:** Calculated the interaction frequency for the top EMR tasks performed by each of the seven nurses over the study period.
3.  **Statistical Testing:** Formally tested the uniformity of the workload distribution using a Chi-Square test to determine if observed differences were statistically significant.

---

### Project Artifacts

* `Clinical_Workload_Analysis_Report.pdf`: The full academic paper detailing the statistical analysis and findings.
* `Clinical_Workload_Analysis_Poster.pdf`: The research poster presented at the engineering research competitions.

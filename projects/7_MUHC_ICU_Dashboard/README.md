# MUHC ICU Dashboard for EMR Log Data

### Project Summary

Presented at the **Nexus Informatics Conference**, this project tackles the challenge of monitoring nurse workloads by transforming massive, raw Electronic Medical Record (EMR) log data into actionable insights. I developed an interactive **R Shiny dashboard** to process and visualize EMR usage profiles from the MU Health Care (MUHC) ICU.

This tool provides a framework for researchers and hospital administrators to explore nurse activity patterns, identify workload trends, and investigate the sources of nurse burnout by analyzing millions of log records from a single 12-hour nursing shift.

### Methodology & Technical Stack

* **Primary Tools:** R, R Shiny
* **Core Methodologies:** Data Wrangling, Data Visualization, Dashboard Development, Time-Series Analysis

The dashboard allows users to filter EMR data by individual nurses and visualize key performance indicators, such as the frequency and duration of specific tasks ("timernames"), through various plots and charts.

### Key Features

* **Interactive Filtering:** Users can select individual nurses to analyze their specific EMR usage patterns.
* **Task Frequency Analysis:** The dashboard provides a "Top 10" list of the most frequent EMR tasks, allowing for a quick overview of a nurse's workload.
* **Time-Series Visualization:** The duration of EMR tasks is plotted over time, enabling the identification of trends and peak workload periods.
* **Data-Driven Insights:** The dashboard provides a quantitative basis for understanding the distribution of EMR workload among nurses, which can be used to inform staffing and resource allocation decisions.

### Project Artifacts

* `MUHC-Nurse-Log-Data-Dashboard-Presentation.pdf`: The slide deck presented at the Nexus Informatics Conference.
* `Nurse-Log-Data-Dashboard-Poster.pdf`: The research poster summarizing the project and dashboard features.

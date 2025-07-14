# Healthcare Patient Flow Simulation

### Project Highlights

* **Outcome:** Engineered a predictive simulation model that earned the **Best 2023 Industrial & Systems Engineering Capstone Project** award.
* **Impact:** Provided University of Missouri Health Care executives with a low-cost, low-risk tool to forecast ER bed shortages and test high-stakes operational strategies.
* **My Role:** As team lead, I directed the project from data analysis to final model development, including designing the complex patient routing logic.
* **Challenge:** To create a validated digital twin of the hospital's patient flow to support strategic planning for a projected 5-10% growth in patient volume.

---

### Technical Snapshot

* **Primary Tool:** Simio (Discrete-Event Simulation)
* **Analysis Tools:**  R, NCSS , SQL, Excel (Pivot Tables)
* **Core Methodologies:** Statistical Distribution Fitting, Model Validation, 4-Dimensional Markov Chain (for patient routing)

---

### Model Development & Methodology

Our team built a comprehensive simulation of the hospital by analyzing a dataset of over 87,000 real patient encounters.

1.  **Stochastic Modeling:** We used statistical analysis to fit distributions for key variables like patient arrival rates and length of stay, ensuring the model accurately reflected real-world variability.
2.  **Advanced Routing Logic:** A key innovation was the development of a **4-dimensional Markov chain** to handle complex patient routing. This logic directed simulated patients based on their current unit, next destination, point of origin, and path history, creating a highly realistic flow.
3.  **Validation:** The model's outputs, such as the daily hospital census, were compared against historical data to confirm the model's accuracy and reliability as a predictive tool.

---

### Project Artifacts

* `MUHC_Patient_Flow_Simulation_Report.pdf`: The final capstone report detailing the project methodology and findings.
* `MUHC_Patient_Flow_Simulation_Presentation.pdf`: The slide deck presented for the capstone project.

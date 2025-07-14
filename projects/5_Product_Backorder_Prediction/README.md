# Predicting Product Backorders with Anomaly Detection

### Project Highlights

* **Challenge:** Analyzed a large-scale dataset of ~1.9 million product observations to proactively predict which items are at risk of going on backorder. The goal was to reduce costly stock-outs and improve customer satisfaction.
* **Methodology:** Developed and benchmarked three unique machine learning pipelines. The optimal model uses **Isolation Forest** for outlier detection, **Principal Component Analysis (PCA)** for dimensionality reduction, and a **Random Forest** for classification.
* **Results:** The final model successfully identifies **74% of all true backorders** (Recall) on unseen data with an **82% overall accuracy**, enabling a shift from reactive to proactive inventory management.

---

### The Winning Pipeline

The best-performing model was a three-step pipeline that systematically processes the data to make a prediction:

1.  **Anomaly Detection (`IsolationForest`):** First, outliers (2% of the data) were removed from the training set. This creates a cleaner dataset, leading to a more robust and reliable classification model.
2.  **Dimensionality Reduction (`PCA`):** The initial 22 predictor variables were scaled and then condensed into 15 principal components, capturing the most important information while increasing training speed and efficiency.
3.  **Classification (`RandomForest`):** An ensemble of 400 decision trees (with a max depth of 20) was trained on the pre-processed data to vote on the final backorder risk for each product.

---

### Business Impact

This predictive system allows inventory planners to shift from **reactive firefighting** to **proactive planning.** Instead of manually monitoring all SKUs, planners can focus on a targeted list of at-risk items flagged by the model. By catching 74% of all backorders before they happen, this system has the potential to generate over **$600,000 in annual cost savings** while significantly improving customer loyalty.

---

### Files in This Directory

* `Anomaly Detection-Preprocessing.ipynb`: The Jupyter Notebook covering all data loading, cleaning, and sampling steps.
* `Anomaly Detection-Model Development.ipynb`: The Jupyter Notebook where three distinct pipelines were built, tuned, and compared.
* `Anomaly Detection-Evaluation.ipynb`: The Jupyter Notebook used for the final, unbiased evaluation of the winning model against a true test set.

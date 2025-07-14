# Product Backorder Prediction

### Project Summary

This project addresses the critical business problem of predicting product backorders to reduce stock-outs and improve customer satisfaction. By analyzing a large-scale dataset of ~1.9 million product observations, I developed and benchmarked three unique machine learning pipelines to identify the optimal predictive model.

The final model successfully identifies **74% of all true backorders** (Recall) on unseen data with an **82% overall accuracy**. This system enables a shift from reactive firefighting to proactive inventory planning, with a potential for over **$600,000 in annual cost savings**.

---

### Technical Stack & Methodology

* **Language & Libraries:** Python (Pandas, Scikit-learn, NumPy, Joblib)
* **Core Methodologies:** Classification, Anomaly Detection (Isolation Forest), Dimensionality Reduction (PCA), Hyperparameter Tuning (GridSearchCV)

The winning pipeline systematically processes the data to make a prediction:

1.  **Anomaly Detection (`IsolationForest`):** Outliers are removed from the training set to create a cleaner, more robust dataset.
2.  **Dimensionality Reduction (`PCA`):** The 22 predictor variables are condensed into 15 principal components to increase training efficiency.
3.  **Classification (`RandomForest`):** An optimized Random Forest Classifier (400 trees, max depth 20) votes on the final backorder risk for each product.

---

### Project Notebooks

* `Backorder_Prediction_Summary.pdf`: A one-page PDF summary of the project.
* `Backorder_Prediction_Preprocessing.ipynb`: Jupyter Notebook covering all data loading, cleaning, and sampling steps.
* `Backorder_Prediction_Model_Development.ipynb`: Jupyter Notebook where three distinct pipelines were built, tuned, and compared.
* `Backorder_Prediction_Evaluation.ipynb`: Jupyter Notebook for the final, unbiased evaluation of the winning model against a true test set.

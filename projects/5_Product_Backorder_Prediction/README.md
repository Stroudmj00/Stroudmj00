# Product Backorder Prediction

### Project Summary

This project addresses a critical business problem: **predicting product backorders to reduce stock-outs and improve customer satisfaction**. By analyzing a large-scale dataset of ~1.9 million product observations, I developed and benchmarked three unique machine learning pipelines to identify the optimal predictive model.

The final model, a `RandomForestClassifier` combined with `IsolationForest` for anomaly detection and `PCA` for dimensionality reduction, **successfully identifies 74% of all true backorders** (Recall) on unseen data with an **82% overall accuracy**. This system enables a shift from reactive firefighting to proactive inventory planning, with a potential for over **$600,000 in annual cost savings**.

### Technical Stack & Methodology

* **Language & Libraries:** Python (Pandas, Scikit-learn, NumPy, Joblib)
* **Core Methodologies:** Classification, Anomaly Detection (`IsolationForest`), Dimensionality Reduction (`PCA`), Hyperparameter Tuning (`GridSearchCV`)

The winning pipeline systematically processes the data to make a prediction:

1.  **Anomaly Detection (`IsolationForest`):** Outliers are removed from the training set to create a cleaner, more robust dataset.
2.  **Dimensionality Reduction (`PCA`):** The 22 predictor variables are condensed into 15 principal components to increase training efficiency.
3.  **Classification (`RandomForest`):** An optimized Random Forest Classifier (400 trees, max depth 20) votes on the final backorder risk for each product.

### Key Findings & Business Impact

* **High Recall:** The model correctly identifies **74% of all true backorders**, giving the business a significant lead time to address potential stock-outs.
* **High Accuracy:** With an **82% overall accuracy**, the model provides a reliable "heads-up" on likely backorder items.
* **Cost Savings:** By preventing an estimated 74% of the 2,688 annual backorders, each costing an estimated $320, the model has the potential to save the company over **$636,000 per year**.
* **Operational Efficiency:** The model enables inventory planners to focus on a targeted list of at-risk SKUs instead of manually scanning all 240,000 SKUs.

### Project Notebooks

* `Backorder_Prediction_Preprocessing.ipynb`: Jupyter Notebook covering all data loading, cleaning, and sampling steps.
* `Backorder_Prediction_Model_Development.ipynb`: Jupyter Notebook where three distinct pipelines were built, tuned, and compared.
* `Backorder_Prediction_Evaluation.ipynb`: Jupyter Notebook for the final, unbiased evaluation of the winning model against a true test set.

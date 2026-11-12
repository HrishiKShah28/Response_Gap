# Predictive Modeling & Evaluation Report

## 1. Out-of-Time Performance Comparison

| Model Architecture | Chronological ROC-AUC | PR-AUC | Recall (Sensitivity) | Precision | F1-Score | Accuracy | Brier Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Majority Class (Zero-R)** | 0.500 | 0.174 | 0.0% | 0.0% | 0.0% | 82.6% | 0.030 |
| **Agency-Prior Lookup** | - | - | 26.4% | 67.0% | 37.9% | 85.0% | - |
| **Regularized Logistic Regression** | **0.933** | **0.747** | **85.3%** | 56.1% | **67.7%** | 85.8% | 0.107 |
| **Gradient Boosted Trees (Champion)**| **0.935** | **0.746** | **85.4%** | **57.2%** | **68.6%** | **86.4%** | **0.102** |

## 2. Confusion Matrix (Gradient Boosted Trees, Out-of-Time Test Set)

- **True Negatives (Resolved <= 7d, Predicted Quick)**: 21,012
- **False Positives (Resolved <= 7d, Flagged Delayed)**: 3,258
- **False Negatives (Delayed > 7d, Missed by Model)**: 743
- **True Positives (Delayed > 7d, Successfully Flagged)**: 4,361

## 3. Operational Triage Interpretation
The Gradient Boosted model captures **over 75% of severely delayed civic complaints** at the instant of intake, allowing city supervisors to initiate proactive field inspection and case routing before statutory 7-day deadlines are breached. While a naive baseline achieves 80%+ accuracy by ignoring all backlogged complaints, it provides zero operational value.
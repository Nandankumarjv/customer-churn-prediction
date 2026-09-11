# Customer Churn Prediction

A machine learning project that predicts whether a customer is likely to churn based on customer demographics, service usage, billing information, and customer support interactions.

The project demonstrates an end-to-end supervised machine learning workflow including data cleaning, exploratory data analysis, preprocessing pipelines, model comparison, hyperparameter tuning, class imbalance handling, threshold optimization, and model serialization.

---

## Project Overview

Customer churn prediction is a binary classification problem where the goal is to identify customers who are likely to leave a service.

In this project, machine learning models are trained to predict:

- `0` → Customer will not churn
- `1` → Customer will churn

The project focuses on building a complete and reusable ML pipeline rather than only training a classification model.

---

## Dataset

The dataset contains customer-level information such as:

### Numerical Features

- Age
- Tenure in months
- Monthly charges
- Total charges
- Number of support calls
- Satisfaction score
- Monthly usage in GB

### Categorical Features

- Contract type
- Payment method
- Internet service
- Streaming
- Auto payment
- Tech support

### Target

- `churn` — Yes / No

The dataset contains missing values, duplicate records, and inconsistent categorical values to simulate common real-world data-cleaning scenarios.

---

## Project Workflow

The project follows the following machine learning workflow:

```text
Data Loading
     ↓
Data Inspection
     ↓
Duplicate Removal
     ↓
Data Cleaning
     ↓
Exploratory Data Analysis
     ↓
Feature / Target Separation
     ↓
Train-Test Split
     ↓
Preprocessing Pipeline
     ↓
Model Training
     ↓
Model Evaluation
     ↓
Hyperparameter Tuning
     ↓
Threshold Optimization
     ↓
Final Prediction
     ↓
Model Serialization
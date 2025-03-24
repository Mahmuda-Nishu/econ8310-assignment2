# -*- coding: utf-8 -*-
"""assignment2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10amAjeH1rmyShztPSzH2feEc1J8e_sKk
"""

# assignment2.py

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import xgboost as xgb

# Load training data
train_url = "https://github.com/dustywhite7/Econ8310/raw/master/AssignmentData/assignment3.csv"
df_train = pd.read_csv(train_url)
df_train = df_train.drop(['id', 'DateTime'], axis=1)

# Define features and label
X_train = df_train.drop('meal', axis=1)
y_train = df_train['meal']

# Define all models to evaluate
cv_models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'XGBClassifier': xgb.XGBClassifier(random_state=42, eval_metric='logloss'),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42)
}

# Evaluate models using cross-validation
cv_scores = {}
print("Cross-Validation Accuracy Scores:")
for name, model_candidate in cv_models.items():
    scores = cross_val_score(model_candidate, X_train, y_train, cv=5, scoring='accuracy')
    cv_scores[name] = np.mean(scores)
    print(f"{name}: {cv_scores[name]:.4f}")

# Select the best-performing model
best_model_name = max(cv_scores, key=cv_scores.get)
print("\nBest model based on CV accuracy:", best_model_name)

# Initialize and train the best model
model = cv_models[best_model_name]
modelFit = model.fit(X_train, y_train)

# Load test data
test_url = "https://github.com/dustywhite7/Econ8310/raw/master/AssignmentData/assignment3test.csv"
df_test = pd.read_csv(test_url)
df_test = df_test.drop(['id', 'DateTime'], axis=1)
df_test = df_test.drop('meal', axis=1, errors='ignore')  # In case 'meal' is present

# Make predictions on test data
predictions = modelFit.predict(df_test)

# Convert to list of 0s and 1s as required
pred = [int(p) for p in predictions]

# Output checks
print("Length of pred:", len(pred))
print("First 10 predictions:", pred[:10])
"""
SpaceX Machine Learning Prediction - Optimized Version
========================================================
This script trains and evaluates multiple machine learning models to predict 
SpaceX Falcon 9 first stage landing success.

Models evaluated:
- Logistic Regression
- Support Vector Machine (SVM)
- Decision Tree
- K-Nearest Neighbors (KNN)

Author: IBM Capstone Project
Optimized: 2026
"""

#%% INITIALIZATION
print("="*60)
print("🚀 SpaceX Machine Learning Prediction Analysis")
print("="*60)
print("Training multiple models to predict landing success...")
print()

# Core libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Scikit-learn imports
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    roc_auc_score, roc_curve, log_loss
)

# System utilities
import sys
import gc
import time
import warnings
from pathlib import Path
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Project path resolution
PROJECT_NAME = "IBM"
cwd = Path.cwd()
try:
    project_root = cwd if cwd.name.upper() == PROJECT_NAME else next(
        p for p in cwd.parents if p.name.upper() == PROJECT_NAME
    )
except StopIteration:
    project_root = cwd
    print(f"⚠️  Warning: Project root '{PROJECT_NAME}' not found. Using current directory.")

sys.path.insert(0, str(project_root))

# Create standard directories
data_dir = project_root / "data"
output_dir = project_root / "outputs"
log_dir = project_root / "logs"

for directory in (data_dir, output_dir, log_dir):
    directory.mkdir(parents=True, exist_ok=True)

print(f"📁 Project root: {project_root}")
print(f"📁 Data directory: {data_dir}")
print(f"📁 Output directory: {output_dir}")
print()

# Start performance timer
start_time = time.perf_counter()


#%% UTILITY FUNCTIONS

def plot_confusion_matrix(y_true, y_pred, title="Confusion Matrix"):
    """
    Plot a confusion matrix with proper formatting.
    
    Parameters:
    -----------
    y_true : array-like
        True labels
    y_pred : array-like
        Predicted labels
    title : str
        Title for the plot
    """
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, cbar_kws={'label': 'Count'})
    
    ax.set_xlabel('Predicted Labels', fontsize=12, fontweight='bold')
    ax.set_ylabel('True Labels', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.xaxis.set_ticklabels(['Did Not Land', 'Landed'])
    ax.yaxis.set_ticklabels(['Did Not Land', 'Landed'])
    
    plt.tight_layout()
    plt.show()


def calculate_metrics(y_true, y_pred, y_pred_proba=None, model_name="Model"):
    """
    Calculate comprehensive performance metrics for a classifier.
    
    Parameters:
    -----------
    y_true : array-like
        True labels
    y_pred : array-like
        Predicted labels
    y_pred_proba : array-like, optional
        Predicted probabilities for positive class
    model_name : str
        Name of the model
    
    Returns:
    --------
    dict : Dictionary containing all performance metrics
    """
    # Basic metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    # Confusion matrix metrics
    cm = confusion_matrix(y_true, y_pred)
    
    if cm.size == 4:
        tn, fp, fn, tp = cm.ravel()
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    else:
        tn, fp, fn, tp = None, None, None, None
        specificity = None
        sensitivity = recall
    
    # Probability-based metrics
    roc_auc = roc_auc_score(y_true, y_pred_proba) if y_pred_proba is not None else None
    logloss = log_loss(y_true, y_pred_proba) if y_pred_proba is not None else None
    
    return {
        'model_name': model_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'specificity': specificity,
        'sensitivity': sensitivity,
        'roc_auc': roc_auc,
        'log_loss': logloss,
        'confusion_matrix': cm,
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn
    }


def print_model_performance(metrics, cv_score=None, best_params=None):
    """
    Print formatted model performance metrics.
    
    Parameters:
    -----------
    metrics : dict
        Dictionary of performance metrics
    cv_score : float, optional
        Cross-validation score
    best_params : dict, optional
        Best hyperparameters from grid search
    """
    print("="*60)
    print(f"{metrics['model_name'].upper()} MODEL PERFORMANCE")
    print("="*60)
    
    print(f"\n📊 BASIC METRICS:")
    print(f"   Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"   Precision: {metrics['precision']:.4f}")
    print(f"   Recall:    {metrics['recall']:.4f}")
    print(f"   F1-Score:  {metrics['f1_score']:.4f}")
    
    if metrics['tp'] is not None:
        print(f"\n🎯 CONFUSION MATRIX METRICS:")
        print(f"   True Positives:  {metrics['tp']}")
        print(f"   True Negatives:  {metrics['tn']}")
        print(f"   False Positives: {metrics['fp']}")
        print(f"   False Negatives: {metrics['fn']}")
        print(f"   Sensitivity:     {metrics['sensitivity']:.4f}")
        print(f"   Specificity:     {metrics['specificity']:.4f}")
    
    if metrics['roc_auc'] is not None:
        print(f"\n📈 PROBABILITY METRICS:")
        print(f"   ROC AUC Score: {metrics['roc_auc']:.4f}")
        if metrics['log_loss'] is not None:
            print(f"   Log Loss:      {metrics['log_loss']:.4f}")
    
    if cv_score is not None:
        print(f"\n🔍 CROSS-VALIDATION:")
        print(f"   CV Accuracy: {cv_score:.4f}")
    
    if best_params is not None:
        print(f"\n⚙️  BEST HYPERPARAMETERS:")
        for param, value in best_params.items():
            print(f"   {param}: {value}")
    
    print()


#%% DATA LOADING

print("📂 Loading data...")

# Load datasets
try:
    data = pd.read_csv(data_dir / "dataset_part_2.csv")
    X_raw = pd.read_csv(data_dir / "dataset_part_3.csv")
    print(f"✅ Loaded {len(data)} samples with {len(X_raw.columns)} features")
except FileNotFoundError as e:
    print(f"❌ Error: Could not find required data files in {data_dir}")
    print(f"   Please ensure 'dataset_part_2.csv' and 'dataset_part_3.csv' exist.")
    sys.exit(1)

print(f"   Target distribution: {dict(pd.Series(data['Class']).value_counts())}")
print()


#%% DATA PREPROCESSING

print("🔧 Preprocessing data...")

# Extract target variable
Y = data["Class"].to_numpy()

# Standardize features
scaler = preprocessing.StandardScaler()
X = scaler.fit_transform(X_raw)

print(f"✅ Features standardized (mean=0, std=1)")

# Train-test split with stratification
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=42,  # Changed to 42 for better reproducibility
    stratify=Y
)

print(f"✅ Data split: {len(X_train)} train, {len(X_test)} test samples")
print(f"   Train class distribution: {dict(pd.Series(Y_train).value_counts())}")
print(f"   Test class distribution:  {dict(pd.Series(Y_test).value_counts())}")
print()

# Validation check
validation_df = pd.DataFrame({
    "Dataset": ["Train", "Test"],
    "Samples": [X_train.shape[0], X_test.shape[0]],
    "Features": [X_train.shape[1], X_test.shape[1]],
    "Target Shape": [Y_train.shape, Y_test.shape],
    "Validation": ["✓" if X_train.shape[0] == Y_train.shape[0] else "✗",
                   "✓" if X_test.shape[0] == Y_test.shape[0] else "✗"]
})

print("📋 Data Validation:")
print(validation_df.to_string(index=False))
print()


#%% INITIALIZE RESULTS STORAGE

# Dictionary to store all model results
all_models_results = {}

# Initialize comparison DataFrame
metrics_df = pd.DataFrame({
    'Metric': [
        'Accuracy', 'Precision', 'Recall', 'F1-Score',
        'CV Accuracy', 'Specificity', 'Sensitivity',
        'ROC AUC', 'Log Loss'
    ]
})


#%% LOGISTIC REGRESSION

print("="*60)
print("🔵 Training Logistic Regression")
print("="*60)

# Hyperparameter grid
lr_params = {
    "C": [0.01, 0.1, 1, 10, 100],  # Expanded search range
    "solver": ["lbfgs", "liblinear"],  # Added liblinear for small datasets
    "max_iter": [1000]
}

# Grid search with cross-validation
lr_model = LogisticRegression(random_state=42)
lr_cv = GridSearchCV(
    estimator=lr_model,
    param_grid=lr_params,
    cv=10,
    n_jobs=-1,
    verbose=0,
    scoring='accuracy'
)

print("⏳ Running grid search with 10-fold cross-validation...")
lr_cv.fit(X_train, Y_train)

# Get best model
best_lr = lr_cv.best_estimator_

# Predictions
y_pred_lr = best_lr.predict(X_test)
y_pred_proba_lr = best_lr.predict_proba(X_test)[:, 1]

# Calculate metrics
lr_metrics = calculate_metrics(Y_test, y_pred_lr, y_pred_proba_lr, "Logistic Regression")
lr_metrics['cv_accuracy'] = lr_cv.best_score_
lr_metrics['best_params'] = lr_cv.best_params_

# Print results
print_model_performance(lr_metrics, lr_cv.best_score_, lr_cv.best_params_)

# Store results
all_models_results['Logistic Regression'] = lr_metrics

# Add to comparison DataFrame
metrics_df['Logistic Regression'] = [
    f"{lr_metrics['accuracy']:.4f}",
    f"{lr_metrics['precision']:.4f}",
    f"{lr_metrics['recall']:.4f}",
    f"{lr_metrics['f1_score']:.4f}",
    f"{lr_metrics['cv_accuracy']:.4f}",
    f"{lr_metrics['specificity']:.4f}",
    f"{lr_metrics['sensitivity']:.4f}",
    f"{lr_metrics['roc_auc']:.4f}",
    f"{lr_metrics['log_loss']:.4f}"
]

# Plot confusion matrix
plot_confusion_matrix(Y_test, y_pred_lr, "Logistic Regression - Confusion Matrix")


#%% SUPPORT VECTOR MACHINE

print("="*60)
print("🟠 Training Support Vector Machine")
print("="*60)

# Hyperparameter grid (optimized for faster training)
svm_params = {
    "kernel": ["linear", "rbf"],  # Removed poly and sigmoid for speed
    "C": [0.1, 1, 10],  # Reduced range
    "gamma": ["scale", "auto"]  # Using string values instead of logspace
}

# Grid search with cross-validation
svm_model = SVC(probability=True, random_state=42)  # Added probability=True
svm_cv = GridSearchCV(
    estimator=svm_model,
    param_grid=svm_params,
    cv=10,
    n_jobs=-1,
    verbose=0,
    scoring='accuracy'
)

print("⏳ Running grid search with 10-fold cross-validation...")
svm_cv.fit(X_train, Y_train)

# Get best model
best_svm = svm_cv.best_estimator_

# Predictions
y_pred_svm = best_svm.predict(X_test)
y_pred_proba_svm = best_svm.predict_proba(X_test)[:, 1]

# Calculate metrics
svm_metrics = calculate_metrics(Y_test, y_pred_svm, y_pred_proba_svm, "Support Vector Machine")
svm_metrics['cv_accuracy'] = svm_cv.best_score_
svm_metrics['best_params'] = svm_cv.best_params_

# Print results
print_model_performance(svm_metrics, svm_cv.best_score_, svm_cv.best_params_)

# Store results
all_models_results['SVM'] = svm_metrics

# Add to comparison DataFrame
metrics_df['SVM'] = [
    f"{svm_metrics['accuracy']:.4f}",
    f"{svm_metrics['precision']:.4f}",
    f"{svm_metrics['recall']:.4f}",
    f"{svm_metrics['f1_score']:.4f}",
    f"{svm_metrics['cv_accuracy']:.4f}",
    f"{svm_metrics['specificity']:.4f}",
    f"{svm_metrics['sensitivity']:.4f}",
    f"{svm_metrics['roc_auc']:.4f}",
    'N/A'  # SVM with probability=True has ROC AUC but typically doesn't report log loss
]

# Plot confusion matrix
plot_confusion_matrix(Y_test, y_pred_svm, "SVM - Confusion Matrix")


#%% DECISION TREE

print("="*60)
print("🟢 Training Decision Tree")
print("="*60)

# Hyperparameter grid
tree_params = {
    "criterion": ["gini", "entropy"],
    "splitter": ["best", "random"],
    "max_depth": [2, 4, 6, 8, 10, 12, 14, 16],  # Simplified range
    "max_features": ["sqrt", None],
    "min_samples_leaf": [1, 2, 4],
    "min_samples_split": [2, 5, 10]
}

# Grid search with cross-validation
tree_model = DecisionTreeClassifier(random_state=42)
tree_cv = GridSearchCV(
    estimator=tree_model,
    param_grid=tree_params,
    cv=10,
    n_jobs=-1,
    verbose=0,
    scoring='accuracy'
)

print("⏳ Running grid search with 10-fold cross-validation...")
tree_cv.fit(X_train, Y_train)

# Get best model
best_tree = tree_cv.best_estimator_

# Predictions
y_pred_tree = best_tree.predict(X_test)
y_pred_proba_tree = best_tree.predict_proba(X_test)[:, 1]

# Calculate metrics
tree_metrics = calculate_metrics(Y_test, y_pred_tree, y_pred_proba_tree, "Decision Tree")
tree_metrics['cv_accuracy'] = tree_cv.best_score_
tree_metrics['best_params'] = tree_cv.best_params_

# Print results
print_model_performance(tree_metrics, tree_cv.best_score_, tree_cv.best_params_)

# Store results
all_models_results['Decision Tree'] = tree_metrics

# Add to comparison DataFrame
metrics_df['Decision Tree'] = [
    f"{tree_metrics['accuracy']:.4f}",
    f"{tree_metrics['precision']:.4f}",
    f"{tree_metrics['recall']:.4f}",
    f"{tree_metrics['f1_score']:.4f}",
    f"{tree_metrics['cv_accuracy']:.4f}",
    f"{tree_metrics['specificity']:.4f}",
    f"{tree_metrics['sensitivity']:.4f}",
    f"{tree_metrics['roc_auc']:.4f}",
    'N/A'
]

# Plot confusion matrix
plot_confusion_matrix(Y_test, y_pred_tree, "Decision Tree - Confusion Matrix")


#%% K-NEAREST NEIGHBORS

print("="*60)
print("🟣 Training K-Nearest Neighbors")
print("="*60)

# Hyperparameter grid
knn_params = {
    "n_neighbors": [1, 3, 5, 7, 9, 11, 15],  # Optimized range
    "algorithm": ["auto", "ball_tree", "kd_tree"],  # Removed brute for speed
    "p": [1, 2],
    "weights": ["uniform", "distance"]  # Added weights parameter
}

# Grid search with cross-validation
knn_model = KNeighborsClassifier()
knn_cv = GridSearchCV(
    estimator=knn_model,
    param_grid=knn_params,
    cv=10,
    n_jobs=-1,
    verbose=0,
    scoring='accuracy'
)

print("⏳ Running grid search with 10-fold cross-validation...")
knn_cv.fit(X_train, Y_train)

# Get best model
best_knn = knn_cv.best_estimator_

# Predictions
y_pred_knn = best_knn.predict(X_test)
y_pred_proba_knn = best_knn.predict_proba(X_test)[:, 1]

# Calculate metrics
knn_metrics = calculate_metrics(Y_test, y_pred_knn, y_pred_proba_knn, "K-Nearest Neighbors")
knn_metrics['cv_accuracy'] = knn_cv.best_score_
knn_metrics['best_params'] = knn_cv.best_params_

# Print results
print_model_performance(knn_metrics, knn_cv.best_score_, knn_cv.best_params_)

# Store results
all_models_results['KNN'] = knn_metrics

# Add to comparison DataFrame
metrics_df['KNN'] = [
    f"{knn_metrics['accuracy']:.4f}",
    f"{knn_metrics['precision']:.4f}",
    f"{knn_metrics['recall']:.4f}",
    f"{knn_metrics['f1_score']:.4f}",
    f"{knn_metrics['cv_accuracy']:.4f}",
    f"{knn_metrics['specificity']:.4f}",
    f"{knn_metrics['sensitivity']:.4f}",
    f"{knn_metrics['roc_auc']:.4f}",
    'N/A'
]

# Plot confusion matrix
plot_confusion_matrix(Y_test, y_pred_knn, "KNN - Confusion Matrix")


#%% MODEL COMPARISON AND FINAL RESULTS

print("\n" + "="*80)
print("📊 FINAL MODEL COMPARISON")
print("="*80)

print("\n" + metrics_df.to_string(index=False))

# Identify best model by test accuracy
best_model_name = max(all_models_results.keys(), 
                      key=lambda k: all_models_results[k]['accuracy'])
best_model_accuracy = all_models_results[best_model_name]['accuracy']

print(f"\n🏆 BEST MODEL: {best_model_name}")
print(f"   Test Accuracy: {best_model_accuracy:.4f} ({best_model_accuracy*100:.2f}%)")

# Identify best model by CV accuracy
best_cv_model_name = max(all_models_results.keys(), 
                         key=lambda k: all_models_results[k]['cv_accuracy'])
best_cv_accuracy = all_models_results[best_cv_model_name]['cv_accuracy']

print(f"\n🎯 BEST CV SCORE: {best_cv_model_name}")
print(f"   CV Accuracy: {best_cv_accuracy:.4f} ({best_cv_accuracy*100:.2f}%)")


#%% SAVE RESULTS

print("\n" + "="*60)
print("💾 Saving Results")
print("="*60)

# Save comparison table
output_file = output_dir / f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
metrics_df.to_csv(output_file, index=False)
print(f"✅ Saved comparison table to: {output_file}")

# Save detailed results as JSON-like format
results_file = output_dir / f"detailed_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(results_file, 'w') as f:
    f.write("SpaceX Landing Prediction - Detailed Results\n")
    f.write("=" * 60 + "\n\n")
    
    for model_name, metrics in all_models_results.items():
        f.write(f"\n{model_name}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Accuracy:     {metrics['accuracy']:.4f}\n")
        f.write(f"Precision:    {metrics['precision']:.4f}\n")
        f.write(f"Recall:       {metrics['recall']:.4f}\n")
        f.write(f"F1-Score:     {metrics['f1_score']:.4f}\n")
        f.write(f"CV Accuracy:  {metrics['cv_accuracy']:.4f}\n")
        f.write(f"Specificity:  {metrics['specificity']:.4f}\n")
        f.write(f"Sensitivity:  {metrics['sensitivity']:.4f}\n")
        if metrics['roc_auc']:
            f.write(f"ROC AUC:      {metrics['roc_auc']:.4f}\n")
        f.write(f"Best Params:  {metrics['best_params']}\n")

print(f"✅ Saved detailed results to: {results_file}")


#%% PERFORMANCE SUMMARY

elapsed_time = time.perf_counter() - start_time
print("\n" + "="*60)
print("⏱️  PERFORMANCE SUMMARY")
print("="*60)
print(f"Total execution time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
print(f"Memory objects: {gc.get_count()[0]:,}")

print("\n" + "="*60)
print("✅ Analysis Complete!")
print("="*60)
print("Thank you for using the SpaceX ML Prediction system! 🚀")
print()

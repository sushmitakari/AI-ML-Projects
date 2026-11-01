"""
Model Training, Tuning & Experimentation Tracking Script
Trains multiple ML algorithms, tunes hyperparameters, evaluates performance, and saves the best model.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)

# Optional XGBoost import
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

def train_and_tune_models(data_dir: str = 'data', models_dir: str = 'models'):
    print('==================================================')
    print('       MODEL TRAINING & EXPERIMENT TRACKING       ')
    print('==================================================')
    
    os.makedirs(models_dir, exist_ok=True)
    
    train_path = os.path.join(data_dir, 'train.csv')
    test_path = os.path.join(data_dir, 'test.csv')
    
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print('[ERROR] train.csv or test.csv missing. Run data_preparation.py first.')
        sys.exit(1)
        
    print(f'[INFO] Loading train dataset: {train_path}')
    print(f'[INFO] Loading test dataset:  {test_path}')
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    target_col = 'Engine Condition'
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]
    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]
    
    model_configs = {
        'Decision Tree': {
            'model': DecisionTreeClassifier(random_state=42),
            'params': {
                'max_depth': [3, 5, 10, None],
                'min_samples_split': [2, 5, 10],
                'criterion': ['gini', 'entropy']
            }
        },
        'Random Forest': {
            'model': RandomForestClassifier(random_state=42),
            'params': {
                'n_estimators': [50, 100],
                'max_depth': [5, 10, None],
                'min_samples_split': [2, 5]
            }
        },
        'AdaBoost': {
            'model': AdaBoostClassifier(random_state=42),
            'params': {
                'n_estimators': [50, 100],
                'learning_rate': [0.01, 0.1, 1.0]
            }
        },
        'Gradient Boosting': {
            'model': GradientBoostingClassifier(random_state=42),
            'params': {
                'n_estimators': [50, 100],
                'learning_rate': [0.05, 0.1],
                'max_depth': [3, 5]
            }
        }
    }
    
    if HAS_XGBOOST:
        model_configs['XGBoost'] = {
            'model': XGBClassifier(random_state=42, eval_metric='logloss'),
            'params': {
                'n_estimators': [50, 100],
                'learning_rate': [0.05, 0.1],
                'max_depth': [3, 6]
            }
        }
    else:
        print('[INFO] XGBoost not installed locally; proceeding with standard tree and ensemble models.')
    
    results = {}
    best_model_name = None
    best_f1_score = -1.0
    best_estimator = None
    
    print('\n--- Starting Experimentation & Grid Search Tuning ---')
    for name, config in model_configs.items():
        print(f'\n[TRAINING] {name}...')
        grid = GridSearchCV(
            estimator=config['model'],
            param_grid=config['params'],
            cv=5,
            scoring='f1',
            n_jobs=-1
        )
        grid.fit(X_train, y_train)
        
        best_est = grid.best_estimator_
        y_pred = best_est.predict(X_test)
        y_pred_proba = best_est.predict_proba(X_test)[:, 1] if hasattr(best_est, 'predict_proba') else None
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else 0.0
        
        results[name] = {
            'best_params': grid.best_params_,
            'cv_best_score_f1': float(grid.best_score_),
            'test_accuracy': float(acc),
            'test_precision': float(prec),
            'test_recall': float(rec),
            'test_f1': float(f1),
            'test_roc_auc': float(roc)
        }
        
        print(f'  Best Hyperparameters: {grid.best_params_}')
        print(f'  Test Metrics -> Acc: {acc:.4f} | Prec: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f} | ROC-AUC: {roc:.4f}')
        
        if f1 > best_f1_score:
            best_f1_score = f1
            best_model_name = name
            best_estimator = best_est
            
    print('\n==================================================')
    print(f'[CHAMPION MODEL] Selected Best Model: {best_model_name} (F1 Score: {best_f1_score:.4f})')
    print('==================================================')
    
    # Save best model
    best_model_file = os.path.join(models_dir, 'best_model.pkl')
    joblib.dump(best_estimator, best_model_file)
    print(f'[SUCCESS] Saved best model artifact to: {best_model_file}')
    
    # Save metrics & experiment logs
    metrics_file = os.path.join(models_dir, 'experiment_results.json')
    with open(metrics_file, 'w') as f:
        json.dump({
            'champion_model': best_model_name,
            'feature_names': list(X_train.columns),
            'experiments': results
        }, f, indent=4)
    print(f'[SUCCESS] Saved experiment tracking logs to: {metrics_file}')

if __name__ == '__main__':
    train_and_tune_models()

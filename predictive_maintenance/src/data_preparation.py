"""
Data Preparation & Splitting Script
Loads registered data, handles cleaning, splits into train/test sets, and saves artifacts.
"""

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data(input_path: str = 'data/engine_data.csv', output_dir: str = 'data', test_size: float = 0.2, random_state: int = 42):
    print('==================================================')
    print('                 DATA PREPARATION                 ')
    print('==================================================')
    
    os.makedirs(output_dir, exist_ok=True)
    print(f'[INFO] Loading dataset from: {input_path}')
    df = pd.read_csv(input_path)
    
    # Handle duplicates if any
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        print(f'[INFO] Removing {dup_count} duplicate rows...')
        df = df.drop_duplicates()
        
    # Separate Features & Target
    target_col = 'Engine Condition'
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Stratified Train-Test Split
    print(f'[INFO] Performing Stratified Train-Test Split (test_size={test_size}, random_state={random_state})...')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Combine back for saving
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_path = os.path.join(output_dir, 'train.csv')
    test_path = os.path.join(output_dir, 'test.csv')
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f'[SUCCESS] Training set saved to: {train_path} (Shape: {train_df.shape})')
    print(f'[SUCCESS] Testing set saved to:  {test_path} (Shape: {test_df.shape})')
    print('Training Target Distribution:\n', y_train.value_counts(normalize=True).to_dict())
    print('Testing Target Distribution:\n', y_test.value_counts(normalize=True).to_dict())

if __name__ == '__main__':
    prepare_data()

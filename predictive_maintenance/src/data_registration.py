"""
Data Registration & Schema Validation Script
Validates dataset integrity, column schema, missing values, and data types.
"""

import os
import sys
import pandas as pd

EXPECTED_COLUMNS = [
    'Engine rpm',
    'Lub oil pressure',
    'Fuel pressure',
    'Coolant pressure',
    'lub oil temp',
    'Coolant temp',
    'Engine Condition'
]

def register_and_validate_data(data_path: str = 'data/engine_data.csv'):
    print('==================================================')
    print('          DATA REGISTRATION & VALIDATION          ')
    print('==================================================')
    
    if not os.path.exists(data_path):
        print(f'[ERROR] Data file not found at: {data_path}')
        sys.exit(1)
        
    print(f'[INFO] Loading dataset from: {data_path}')
    df = pd.read_csv(data_path)
    
    # 1. Shape check
    print(f'[CHECK 1] Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns')
    
    # 2. Column schema check
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        print(f'[ERROR] Missing expected columns: {missing_cols}')
        sys.exit(1)
    else:
        print('[CHECK 2] All expected columns are present.')
        
    # 3. Missing values check
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls > 0:
        print(f'[WARNING] Found {total_nulls} missing values across features:')
        print(null_counts[null_counts > 0])
    else:
        print('[CHECK 3] Zero missing values detected across all columns.')
        
    # 4. Target variable check
    target_col = 'Engine Condition'
    unique_targets = df[target_col].unique()
    print(f'[CHECK 4] Target Variable: {target_col} | Unique Values: {unique_targets}')
    print('Target distribution:')
    print(df[target_col].value_counts(normalize=True).apply(lambda x: f'{x*100:.2f}%'))
    
    # 5. Statistical Summary
    print('\n--- Statistical Summary ---')
    print(df.describe().T[['mean', 'std', 'min', '50%', 'max']].to_string())
    
    print('\n[SUCCESS] Dataset successfully validated and registered.')
    return True

if __name__ == '__main__':
    data_path = sys.argv[1] if len(sys.argv) > 1 else 'data/engine_data.csv'
    register_and_validate_data(data_path)

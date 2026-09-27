import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np # Needed for NaN handling

df = pd.read_csv("sales_project/data/Superkart.csv") # Updated to Superkart.csv

# 1. Product_ID Feature Engineering: Extract Product_Category (two-letter prefix)
# If Product_Id is 'FD123', Product_Category will be 'FD'
df['Product_Category'] = df['Product_Id'].str[:2]

# 2. Product_Sugar_Content Mapping: Standardize and map
# Handle spelling variations like "reg" and map to numerical values
df['Product_Sugar_Content'] = df['Product_Sugar_Content'].replace({'reg': 'Regular'})
sugar_mapping = {'Low Sugar': 1, 'Regular': 2, 'No Sugar': 3}
df['Product_Sugar_Content_Mapped'] = df['Product_Sugar_Content'].map(sugar_mapping)

# 3. Product_Allocated_Area Imputation: Impute zero values with mean area per Product_Type
df['Product_Allocated_Area'] = pd.to_numeric(df['Product_Allocated_Area'], errors='coerce')
mean_area_per_product_type = df[df['Product_Allocated_Area'] > 0].groupby('Product_Type')['Product_Allocated_Area'].mean()
df['Product_Allocated_Area'] = df.apply(
    lambda row: mean_area_per_product_type[row['Product_Type']] if row['Product_Allocated_Area'] == 0 else row['Product_Allocated_Area'],
    axis=1
)
df['Product_Allocated_Area'] = df['Product_Allocated_Area'].fillna(df['Product_Allocated_Area'].mean())

# 4. Store_Age Calculation: Store_Age = Current_Year - Store_Establishment_Year
CURRENT_YEAR = 2024 # Using a fixed current year
df['Store_Age'] = CURRENT_YEAR - df['Store_Establishment_Year']

# 5. Store_Product_Count: Count distinct products sold per store
store_product_count = df.groupby('Store_Id')['Product_Id'].nunique().reset_index()
store_product_count.rename(columns={'Product_Id': 'Store_Product_Count'}, inplace=True)
df = pd.merge(df, store_product_count, on='Store_Id', how='left')

# 6. Price_Per_Weight: Product_MRP / Product_Weight
df['Price_Per_Weight'] = df['Product_MRP'] / df['Product_Weight']
df['Price_Per_Weight'] = df['Price_Per_Weight'].replace([np.inf, -np.inf], np.nan)
df['Price_Per_Weight'] = df['Price_Per_Weight'].fillna(df['Price_Per_Weight'].mean())

# 7. MRP_Ratio_To_Type_Avg: Relative_MRP = Product_MRP / Mean_MRP_of_Product_Type
mean_mrp_per_product_type = df.groupby('Product_Type')['Product_MRP'].mean().reset_index()
mean_mrp_per_product_type.rename(columns={'Product_MRP': 'Mean_MRP_of_Product_Type'}, inplace=True)
df = pd.merge(df, mean_mrp_per_product_type, on='Product_Type', how='left')
df['Relative_MRP'] = df['Product_MRP'] / df['Mean_MRP_of_Product_Type']
df.drop(columns=['Mean_MRP_of_Product_Type'], inplace=True)
df['Relative_MRP'] = df['Relative_MRP'].replace([np.inf, -np.inf], np.nan)
df['Relative_MRP'] = df['Relative_MRP'].fillna(df['Relative_MRP'].mean())

# 8. Display Efficiency: Sales_Per_Area_Ratio = Product_Store_Sales_Total / Product_Allocated_Area
df['Sales_Per_Area_Ratio'] = df['Product_Store_Sales_Total'] / df['Product_Allocated_Area']
df['Sales_Per_Area_Ratio'] = df['Sales_Per_Area_Ratio'].replace([np.inf, -np.inf], np.nan)
df['Sales_Per_Area_Ratio'] = df['Sales_Per_Area_Ratio'].fillna(df['Sales_Per_Area_Ratio'].mean())

# Drop original identifier columns and any intermediate columns after feature engineering
df.drop(columns=["Product_Id", "Store_Id", "Product_Sugar_Content"], inplace=True)

target_col = "Product_Store_Sales_Total" # Correct target for regression
X = df.drop(columns=[target_col])
y = df[target_col]

# Remove stratify=y for regression task
Xtrain, Xtest, ytrain, ytest = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Save the split data into the 'sales_project/model_building/' directory
Xtrain.to_csv("sales_project/model_building/Xtrain.csv", index=False)
Xtest.to_csv("sales_project/model_building/Xtest.csv", index=False)
ytrain.to_csv("sales_project/model_building/ytrain.csv", index=False, header=True)
ytest.to_csv("sales_project/model_building/ytest.csv", index=False, header=True)

print("Data prepared: train/test splits written.")
# Correct print statement for regression target
print(f"{target_col} statistics in train:")
print(ytrain.describe())

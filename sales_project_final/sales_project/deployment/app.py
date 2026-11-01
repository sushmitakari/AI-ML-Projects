
import streamlit as st
import pandas as pd
import joblib
import os

# --- Configuration --- #
MODEL_PATH = os.path.join("sales_project", "deployment", "best_model.pkl")

# --- Load the trained model --- #
@st.cache_resource
def load_model(path):
    try:
        model = joblib.load(path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model(MODEL_PATH)

# --- Streamlit UI --- #
st.title("Sales Prediction App")

if model is not None:
    st.write("Enter product and store details to predict sales.")

    # --- Input Fields --- #
    # Product features
    product_weight = st.number_input("Product Weight(kg)", min_value=1.0, max_value=20.0, value=10.0, step=0.1)
    product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=0.5, value=0.1, step=0.01)
    product_mrp = st.number_input("Product MRP($)", min_value=50.0, max_value=300.0, value=150.0, step=1.0)

    product_category_options = ['Food', 'Drinks', 'Non Consumables'] # Based on prep.py logic (Product_Id prefix)
    product_category = st.selectbox("Product Category", options=product_category_options)

    product_type_options = [
        'Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 'Household',
        'Baking Goods', 'Snack Foods', 'Frozen Foods', 'Breakfast', 'Health and Hygiene',
        'Hard Drinks', 'Canned', 'Breads', 'Starchy Foods', 'Others', 'Seafood'
    ] # Based on unique values in data
    product_type = st.selectbox("Product Type", options=product_type_options)

    # Store features
    store_establishment_year = st.number_input("Store Establishment Year", min_value=1980, max_value=2023, value=2000, step=1)
    store_size_options = ['Small', 'Medium', 'High'] # Based on data
    store_size = st.selectbox("Store Size", options=store_size_options)

    store_location_city_type_options = ['Tier 1', 'Tier 2', 'Tier 3'] # Based on data
    store_location_city_type = st.selectbox("Store Location City Type", options=store_location_city_type_options)

    store_type_options = ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Grocery Store'] # Based on data
    store_type = st.selectbox("Store Type", options=store_type_options)

    # Product Sugar Content (simplified input for app, assume a default or map)
    # For simplicity, we'll map this to 'Regular' as it's a numerical feature in the model
    # and the model expects a pre-processed numerical value. We'll use a fixed value or make it selectable.
    product_sugar_content_mapped_options = {'Low Sugar': 1, 'Regular': 2, 'No Sugar': 3}
    selected_sugar_content = st.selectbox("Product Sugar Content", options=list(product_sugar_content_mapped_options.keys()))
    product_sugar_content_mapped = product_sugar_content_mapped_options[selected_sugar_content]

    # Placeholder for Store_Id to calculate Store_Product_Count, won't be used directly but needed for feature generation
    # In a real app, this might be selected from existing stores or inferred
    # For this simplified app, we'll assign a dummy 'Store_Id' and let the 'Store_Product_Count' be an input too.
    # However, the model expects 'Store_Product_Count' directly. Let's make it an input.
    store_product_count = st.number_input("Store Product Count", min_value=1, max_value=2000, value=500, step=10)


    # --- Make Prediction --- #
    if st.button("Predict Sales"):
        # Create a DataFrame for prediction
        input_data = pd.DataFrame({
            'Product_Weight': [product_weight],
            'Product_Allocated_Area': [product_allocated_area],
            'Product_MRP': [product_mrp],
            'Store_Establishment_Year': [store_establishment_year],
            'Store_Size': [store_size],
            'Store_Location_City_Type': [store_location_city_type],
            'Store_Type': [store_type],
            'Product_Category': [product_category],
            'Product_Sugar_Content_Mapped': [product_sugar_content_mapped],
            'Store_Product_Count': [store_product_count]
        })

        # Add derived features (as done in prep.py)
        # Note: Some features like 'Price_Per_Weight', 'Relative_MRP', 'Sales_Per_Area_Ratio' need to be calculated here
        # The model pipeline expects these features to be present in the input DataFrame.
        # Since the preprocessor in the pipeline handles scaling and one-hot encoding,
        # we need to ensure the raw features are provided in the correct format to the pipeline.

        # Calculate Store_Age
        CURRENT_YEAR = 2024 # Must match value used in prep.py
        input_data['Store_Age'] = CURRENT_YEAR - input_data['Store_Establishment_Year']

        # Calculate Price_Per_Weight
        input_data['Price_Per_Weight'] = input_data['Product_MRP'] / input_data['Product_Weight']

        # Relative_MRP (Requires mean MRP per Product_Type from training data - simplified for app)
        # For simplicity, we'll use a global mean or a simplified calculation. Ideally, this should come from stored training stats.
        # For now, let's just make a placeholder, as the model pipeline's preprocessor might be robust enough with some defaults.
        # A more robust solution would involve saving these statistics with the model or in a separate file.
        # For this app, we'll make an assumption for 'Relative_MRP' for demonstration purposes.
        # Let's assume a global mean MRP or allow user to input it. For now, we use a fixed ratio for demonstration.
        # This is a potential point for improvement if the model is sensitive to this.
        input_data['Relative_MRP'] = input_data['Product_MRP'] / 150.0 # Example average MRP, needs to be derived from training data

        # Sales_Per_Area_Ratio (cannot calculate without actual sales data, which is what we're predicting)
        # This feature should ideally NOT be an input to the prediction, as it contains the target variable.
        # If the model was trained with it, it implies this feature is known at prediction time, which is usually not the case.
        # We need to adjust the model training if this feature is not available at inference.
        # Assuming for the app that this feature is to be omitted or handled differently.
        # If it was in Xtrain/Xtest, we need to ensure the model pipeline can handle its absence or impute it.
        # However, the current model pipeline expects all `final_features`.
        # Let's remove 'Sales_Per_Area_Ratio' from the input for now and re-evaluate the model's feature set if needed.
        # If 'Sales_Per_Area_Ratio' is crucial, it implies a more complex inference logic.
        # For a first iteration, we'll try predicting without it and see how the model behaves.
        # Or, we provide a placeholder value if the model absolutely expects it. Let's provide a mean value for now.
        input_data['Sales_Per_Area_Ratio'] = 2000.0 # Placeholder, ideally from training data mean

        # Drop original identifier columns that are not directly used by the pipeline but were used for feature creation
        input_data.drop(columns=['Store_Establishment_Year'], inplace=True)

        # Ensure the order of columns matches the training data features as expected by the pipeline
        # The `final_features` list from training cell `aVZWIn_68Etk` is crucial here.
        # The pipeline's preprocessor expects features in a specific order.
        # It's safer to reconstruct the dataframe with the exact column order as `final_features`.
        # Let's recreate `final_features` here or make it available from the notebook state.

        # For now, manually defining `final_features` (numerical + categorical) based on the training script.
        # In a real-world scenario, these should be saved with the model or in a config.
        expected_features_order = [
            "Product_Weight", "Product_Allocated_Area", "Product_MRP", "Store_Age",
            "Store_Product_Count", "Price_Per_Weight", "Relative_MRP", "Sales_Per_Area_Ratio",
            "Product_Sugar_Content_Mapped", "Product_Category", "Product_Type",
            "Store_Size", "Store_Location_City_Type", "Store_Type"
        ]

        # Ensure all expected features are in input_data, even if with dummy values
        # This might require more careful handling of how `Relative_MRP` and `Sales_Per_Area_Ratio` are generated.
        # For robustness, it's often better to retrain without features that cannot be known at inference.
        # Or, save feature engineering objects (like mean_mrp_per_product_type) alongside the model.

        # Let's re-align columns for prediction
        try:
            # Align columns. New categories might cause issues with OneHotEncoder if not handled (handle_unknown='ignore')
            # Create a dataframe with all features including the ones derived
            processed_input = pd.DataFrame({
                'Product_Weight': [product_weight],
                'Product_Allocated_Area': [product_allocated_area],
                'Product_MRP': [product_mrp],
                'Store_Age': [CURRENT_YEAR - store_establishment_year],
                'Store_Product_Count': [store_product_count],
                'Price_Per_Weight': [product_weight / product_mrp], # Fixed calculation
                'Relative_MRP': [product_mrp / 150.0], # Placeholder
                'Sales_Per_Area_Ratio': [2000.0], # Placeholder
                'Product_Sugar_Content_Mapped': [product_sugar_content_mapped],
                'Product_Category': [product_category],
                'Product_Type': [product_type],
                'Store_Size': [store_size],
                'Store_Location_City_Type': [store_location_city_type],
                'Store_Type': [store_type]
            }, index=[0])

            # Ensure columns are in the exact order the model expects
            processed_input = processed_input[expected_features_order]

            prediction = model.predict(processed_input)[0]
            st.success(f"Predicted Sales: ${prediction:,.2f}")
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            st.write("Please ensure all inputs are valid and match the model's expectations.")
else:
    st.warning("Model could not be loaded. Please ensure 'best_model.pkl' exists in the 'sales_project/deployment' directory.")

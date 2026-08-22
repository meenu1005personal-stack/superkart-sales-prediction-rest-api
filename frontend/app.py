import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction") # Updated title

# Section for online prediction
st.subheader("Online Sales Prediction") # Updated subheader

# Collect user input for product features
product_weight = st.number_input("Product Weight", min_value=1.0, value=12.66, step=0.01)
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.001, value=0.027, step=0.001, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=10.0, value=117.08, step=0.01)
store_age_years = st.number_input("Store Age (Years)", min_value=1, value=16)
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
product_id_char = st.selectbox("Product ID Characters", ["FD", "DR", "NC"])
product_type_category = st.selectbox("Product Type Category", ["Perishables", "Drinks", "Non Perishables"])

# Convert user input into a DataFrame
input_data = pd.DataFrame({
    'Product_Weight': [product_weight],
    'Product_Allocated_Area': [product_allocated_area],
    'Product_MRP': [product_mrp],
    'Store_Age_Years': [store_age_years],
    'Product_Sugar_Content': [product_sugar_content],
    'Store_Size': [store_size],
    'Store_Location_City_Type': [store_location_city_type],
    'Store_Type': [store_type],
    'Product_Id_char': [product_id_char],
    'Product_Type_Category': [product_type_category]
})

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict_sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API (Updated endpoint)
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales (in dollars)'] # Updated key
        st.success(f"Predicted Sales (in dollars): {prediction}") # Updated message
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Sales Prediction") # Updated subheader

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predict_sales_batch", files={"file": uploaded_file})  # Send file to Flask API (Updated endpoint)
        if response.status_code == 200:
            predictions = response.json() # Backend now returns {'predictions': [...]}
            st.success("Batch predictions completed!")
            st.write(predictions['predictions'])  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")

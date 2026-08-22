# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("SuperKart Sales Predictor") # Updated app name

# Load the trained machine learning model
model = joblib.load("backend_files/superkart_prediction_model_v1_0.joblib") # Corrected filename and path

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superkart_sales_predictor_api.post('/v1/predict_sales') # Updated endpoint
def predict_sales(): # Updated function name
    """
    This function handles POST requests to the '/v1/predict_sales' endpoint.
    It expects a JSON payload containing product details and returns
    the predicted sales as a JSON response.
    """
    # Get the JSON data from the request body
    product_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Product_Id_char': product_data['Product_Id_char'],
        'Product_Type_Category': product_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales = model.predict(input_data)[0]

    # Convert predicted_sales to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # Return the predicted sales
    return jsonify({'Predicted Sales (in dollars)': predicted_sales})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/predict_sales_batch') # Updated endpoint
def predict_sales_batch(): # Updated function name
    """
    This function handles POST requests to the '/v1/predict_sales_batch' endpoint.
    It expects a CSV file containing product details for multiple products
    and returns the predicted sales as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all products in the DataFrame
    predicted_sales = model.predict(input_data).tolist()

    # Round predictions and ensure float type
    predicted_sales = [round(float(s), 2) for s in predicted_sales]

    # Return the predictions dictionary as a JSON response
    return jsonify({'predictions': predicted_sales})

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)

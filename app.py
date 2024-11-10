from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained machine learning model
model_filename = 'model.pkl'  # Path to your trained model file
scaler_filename = 'scaler.pkl'  # Path to the scaler (StandardScaler) file if used

# Load model and scaler
with open(model_filename, 'rb') as f:
    model = pickle.load(f)

with open(scaler_filename, 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def home():
    return "Flask ML model is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the POST request
        data = request.get_json()

        # Log the received data
        app.logger.debug(f"Received data: {data}")

        # Convert the received data into a pandas DataFrame (with feature names)
        df = pd.DataFrame([data], columns=['Distance', 'Pressure', 'HRV', 'Sugar level', 'SpO2', 'Accelerometer'])

        # Normalize data using the preloaded scaler (StandardScaler)
        X_scaled = scaler.transform(df)

        # Predict using the loaded model
        prediction = model.predict(X_scaled)

        # Log the prediction
        app.logger.debug(f"Prediction: {prediction[0]}")

        # Return the prediction as a JSON response along with the input data
        return jsonify({'prediction': int(prediction[0]), 'input_data': data})

    except Exception as e:
        app.logger.error(f"Error processing prediction: {e}")
        return jsonify({'error': 'Error in prediction processing'}), 500

if __name__ == "__main__":
    app.run(debug=True)

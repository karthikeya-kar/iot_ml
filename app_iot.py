import threading
import time
from flask import Flask, request, jsonify
import queue

app = Flask(__name__)

# Initialize a queue to hold incoming data
data_queue = queue.Queue()

# Function to process the data in the queue
def process_data():
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            print(f"Processing data: {data}")
            
            # Extract values from the incoming data
            distance = data['Distance']
            pressure = data['Pressure']
            hrv = data['HRV']
            sugar_level = data['Sugar level']
            spo2 = data['SpO2']
            accelerometer = data['Accelerometer']

            # Decision logic based on threshold values
            if distance > 50 and pressure == 'Small' and 60 <= hrv <= 90 and 70 <= sugar_level <= 80 and spo2 > 90 and accelerometer == "Below Threshold":
                decision = "No fall. Happy walking!"
            elif distance < 30 and pressure == 'Medium' and 90 <= hrv <= 105 and 30 <= sugar_level <= 70 and 80 <= spo2 <= 90 and accelerometer == "Above Threshold":
                decision = "Take a break, you tripped!"
            elif distance < 10 and pressure == 'Large' and hrv > 105 and (sugar_level < 30 or sugar_level > 160) and spo2 < 80 and accelerometer == "Above Threshold":
                decision = "Definite fall. Help is on the way!"
            else:
                decision = "Unknown situation. Please check values."

            # Simulate processing time (for demo purposes)
            time.sleep(2)  # Simulate delay in processing

            print(f"Decision: {decision}")

# Start the data processing thread
processing_thread = threading.Thread(target=process_data, daemon=True)
processing_thread.start()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the request
        data = request.get_json()
        print(f"Received data: {data}")

        # Put incoming data into the queue for processing
        data_queue.put(data)

        # Respond to the client with a message that data is being processed
        return jsonify({'message': 'Data received, processing in progress.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

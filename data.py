import random
import time
import requests

# Define the URL endpoint for your app's backend
url = 'http://127.0.0.1:5000/predict'

# Function to simulate normal sensor data
def generate_normal_data():
    data = {
        'Distance': round(random.uniform(50, 100), 2),  # Simulate safe distance
        'Pressure': 'Small',
        'HRV': round(random.uniform(60, 90), 2),  # Normal HRV range
        'Sugar level': round(random.uniform(70, 80), 2),  # Normal sugar level
        'SpO2': round(random.uniform(91, 100), 2),  # Normal SpO2 range
        'Accelerometer': "Below Threshold"  # Safe level
    }
    return data

# Function to simulate problematic sensor data every 20 seconds
def generate_problem_data():
    data = {
        'Distance': round(random.uniform(0, 10), 2),  # Dangerous proximity
        'Pressure': 'Large',
        'HRV': round(random.uniform(105, 120), 2),  # High HRV indicating stress or activity
        'Sugar level': round(random.choice([random.uniform(0, 30), random.uniform(160, 200)]), 2),  # Abnormal sugar level
        'SpO2': round(random.uniform(70, 79), 2),  # Low SpO2 indicating possible hypoxia
        'Accelerometer': "Above Threshold"  # Indicating possible fall
    }
    return data

# Send data periodically, with a "problem" every 20 seconds
counter = 0
while True:
    if counter % 4 == 0:  # Every 4th iteration, send problematic data
        simulated_data = generate_problem_data()
        print("Sending PROBLEM data:", simulated_data)
    else:
        simulated_data = generate_normal_data()
        print("Sending normal data:", simulated_data)
    
    # Send the simulated data to the backend server
    response = requests.post(url, json=simulated_data)
    print("Server response:", response.status_code)
    
    # Wait for 5 seconds before sending the next data
    time.sleep(5)
    counter += 1

import os
import json
import matplotlib.pyplot as plt
from twilio.rest import Client

# Load Twilio credentials securely from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'XXXXXXXXXXXXXXXXXXXXXX')  # Replace with your actual SID
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'XXXXXXXXXXXXXXXXXXXX')  # Replace with your actual token
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'XXXXXXXX')  # Replace with your Twilio number

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class EnvironmentalData:
    def __init__(self, initial_data):
        self.data = initial_data

    def get_latest_data(self):
        return self.data

class Alert:
    def __init__(self, parameter, threshold, message, phone_number):
        self.parameter = parameter
        self.threshold = threshold
        self.message = message
        self.phone_number = phone_number

    def check_and_alert(self, data):
        values = data.get(self.parameter, [])
        if any(value >= self.threshold for value in values):
            self.send_alert()

    def send_alert(self):
        try:
            message = twilio_client.messages.create(
                body=self.message,
                from_=TWILIO_PHONE_NUMBER,
                to=self.phone_number
            )
            print(f"Alert sent: {self.message} to {self.phone_number}, SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send alert: {e}")

class UserProfile:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.alerts = []

    def add_alert(self, alert):
        self.alerts.append(alert)

    def check_alerts(self, environmental_data):
        for alert in self.alerts:
            alert.check_and_alert(environmental_data.get_latest_data())

class DataVisualization:
    def __init__(self, data):
        self.data = data

    def plot(self, parameter):
        plt.figure(figsize=(10, 5))
        plt.plot(self.data[parameter], marker='o', label=parameter)
        plt.title(f"{parameter.capitalize()} Data Over Time")
        plt.xlabel("Time Units")
        plt.ylabel(parameter.capitalize())
        plt.legend()
        plt.grid(True)
        plt.show()

def prompt_for_data():
    print("Please enter your name: ")
    name = input()
    print("Please enter your mobile number: ")
    phone_number = input()
    print("Please enter the environmental data in the following format:")
    print(json.dumps({
        "temperature": [22, 23, 24, 28, 32, 31],
        "humidity": [45, 50, 55, 60, 65, 70],
        # Add other parameters here as needed
    }, indent=4))
    data_input = input("Enter data here: ")
    try:
        environmental_data = json.loads(data_input)
    except json.JSONDecodeError:
        print("There was an error decoding your data. Please ensure it is in proper JSON format.")
        return None, None, None
    return name, phone_number, environmental_data

def main():
    name, phone_number, sample_data = prompt_for_data()
    if not sample_data:
        print("No valid environmental data provided.")
        return

    env_data = EnvironmentalData(sample_data)
    user_profile = UserProfile(name, phone_number)

    # Setup dynamic alerts based on predefined conditions
    alert_conditions = {
    "temperature": {"threshold": 30, "message": "High temperature alert!"},
    "humidity": {"threshold": 70, "message": "High humidity alert!"},
    "PM2.5": {"threshold": 25, "message": "High PM2.5 levels detected!"},
    "PM10": {"threshold": 50, "message": "High PM10 levels detected!"},
    "CO2": {"threshold": 1000, "message": "Elevated CO2 levels! Ventilate the area."},
    "NO2": {"threshold": 40, "message": "High NO2 levels detected!"},
    "O3": {"threshold": 180, "message": "High ozone levels detected!"},
    "SO2": {"threshold": 20, "message": "High sulfur dioxide levels detected!"},
    "atmospheric_pressure": {"threshold": 1020, "message": "High atmospheric pressure!"},
    "wind_speed": {"threshold": 25, "message": "High wind speeds detected!"},
    "wind_direction": {"threshold": 360, "message": "Note: Wind direction threshold set to max."},
    "rainfall": {"threshold": 20, "message": "Heavy rainfall detected!"},
    "UV_index": {"threshold": 8, "message": "High UV index detected! Wear sunscreen."}
}


    for parameter, condition in alert_conditions.items():
        if parameter in sample_data:
            user_profile.add_alert(
                Alert(
                    parameter=parameter,
                    threshold=condition["threshold"],
                    message=condition["message"],
                    phone_number=phone_number
                )
            )

    # Check and send alerts if any environmental data exceeds the thresholds
    user_profile.check_alerts(env_data)

    # Visualize all environmental data
    data_visualization = DataVisualization(sample_data)
    for parameter in sample_data:
        data_visualization.plot(parameter)

if __name__ == "__main__":
    main()

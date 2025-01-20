import requests
import random
import time
import re  # Import the regex module for parsing commands


class Sensor:
    def __init__(self, name, min_valtest2.pyue, max_value):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value

    def read_value(self):
        return round(random.uniform(self.min_value, self.max_value), 2)


class Actuator:
    def __init__(self, name):
        self.name = name
        self.state = "OFF"

    def set_state(self, state):
        self.state = state
        print(f"{self.name} set to {self.state}")


def send_to_llm(sensor_values):
    url = "http://100.68.248.159:1234/v1/chat/completions"  # LLM API endpoint
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama-3.2-3b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a control system for managing actuators based on sensor values."
            },
            {
                "role": "user",
                "content": f"Here are the sensor readings: {sensor_values}. Provide commands for actuators in the format: 'Actuator1=ON, Actuator2=OFF'. No other suggestion needed. Just send the commands of actuators."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def parse_llm_response(response_content):
    """Extract actuator commands from LLM response using regex."""
    # Match patterns like 'Actuator1=ON' or 'Actuator2=OFF'
    pattern = r"(\w+=\w+)"
    commands = re.findall(pattern, response_content)
    return commands


def main():
    # Initialize sensors and actuators
    sensors = [
        Sensor("Temperature", 30, 100),
        Sensor("Pressure", 10, 200)
    ]
    actuators = [
        Actuator("Fan"),
        Actuator("Valve")
    ]

    try:
        while True:
            # Gather sensor readings
            sensor_values = {sensor.name: sensor.read_value() for sensor in sensors}
            print(f"Sensor Readings: {sensor_values}")

            # Send sensor data to LLM
            llm_response = send_to_llm(sensor_values)

            if llm_response:
                llm_response_content = llm_response["choices"][0]["message"]["content"]
                print(f"LLM Response: {llm_response_content}")

                # Parse LLM commands
                llm_commands = parse_llm_response(llm_response_content)

                # Execute commands
                for command in llm_commands:
                    actuator_name, state = command.split("=")
                    for actuator in actuators:
                        if actuator.name.lower() == actuator_name.lower():
                            actuator.set_state(state)

            # Wait for the next cycle
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")


if __name__ == "__main__":
    main()

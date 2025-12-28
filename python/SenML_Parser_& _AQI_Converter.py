Python Script: SenML Parser & AQI Converter
Python

import json

# 1. The sample SenML Payload
senml_data = """
[
  {
    "bn": "urn:dev:mac:0024befffe804ff1:",
    "bt": 1735418000,
    "n": "pm2.5",
    "u": "ug/m3",
    "v": 38.5
  },
  {
    "n": "pm10",
    "u": "ug/m3",
    "v": 18.2
  },
  {
    "n": "temperature",
    "u": "Cel",
    "v": 23.4
  }
]
"""

def get_aqi_status(pm25_concentration):
    """
    Returns the AQI Category and Hex Color based on PM2.5 concentration (ug/m3).
    Breakpoints based on US EPA standards.
    """
    # Rounding to match EPA method (integers for AQI, but breakpoints allow decimals)
    c = float(pm25_concentration)

    if c <= 12.0:
        return "Good", "#00E400"  # Green
    elif c <= 35.4:
        return "Moderate", "#FFFF00"  # Yellow
    elif c <= 55.4:
        return "Unhealthy for Sensitive Groups", "#FF7E00"  # Orange
    elif c <= 150.4:
        return "Unhealthy", "#FF0000"  # Red
    elif c <= 250.4:
        return "Very Unhealthy", "#8F3F97"  # Purple
    else:
        return "Hazardous", "#7E0023"  # Maroon

def process_sensor_data(json_payload):
    try:
        data = json.loads(json_payload)
        
        # Iterate through the list to find the PM2.5 record
        pm25_reading = next((item for item in data if item["n"] == "pm2.5"), None)

        if pm25_reading:
            val = pm25_reading['v']
            unit = pm25_reading['u']
            
            # Get status
            category, color_hex = get_aqi_status(val)
            
            print(f"--- Sensor Data Parsed ---")
            print(f"Metric: PM2.5")
            print(f"Reading: {val} {unit}")
            print(f"AQI Status: {category}")
            print(f"Dashboard Color: {color_hex}")
        else:
            print("Error: No PM2.5 data found in payload.")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")

# Run the function
process_sensor_data(senml_data)

import json
import math

# 1. Sample SenML Payload (including Temp & Humidity)
senml_data = """
[
  {
    "bn": "urn:dev:mac:0024befffe804ff1:",
    "bt": 1735418000,
    "n": "pm2.5",
    "u": "ug/m3",
    "v": 12.5
  },
  {
    "n": "temperature",
    "u": "Cel",
    "v": 32.0
  },
  {
    "n": "humidity",
    "u": "%RH",
    "v": 65.0
  }
]
"""

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def calculate_heat_index(temp_c, humidity):
    """
    Calculates Heat Index using NOAA's regression equation.
    Input: Temp in Celsius, Humidity in %.
    Output: Heat Index in Celsius.
    """
    T = celsius_to_fahrenheit(temp_c)
    RH = humidity

    # Simple formula (Steadman) for mild conditions
    HI = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))

    # If the result is 80F or higher, we must use the full Rothfusz regression
    if HI >= 80:
        HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH \
             - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH \
             + .00085282*T*RH*RH - .00000199*T*T*RH*RH
        
        # Adjustment for low humidity conditions
        if (RH < 13) and (T >= 80) and (T <= 112):
            adjustment = ((13-RH)/4)*math.sqrt((17-math.fabs(T-95.))/17)
            HI -= adjustment
        
        # Adjustment for high humidity conditions
        elif (RH > 85) and (T >= 80) and (T <= 87):
            adjustment = ((RH-85)/10) * ((87-T)/5)
            HI += adjustment

    return fahrenheit_to_celsius(HI)

def process_heat_index(json_payload):
    try:
        data = json.loads(json_payload)
        
        # Extract Temp and Humidity safely
        temp_reading = next((item for item in data if item["n"] == "temperature"), None)
        hum_reading = next((item for item in data if item["n"] == "humidity"), None)

        if temp_reading and hum_reading:
            t_val = temp_reading['v']
            h_val = hum_reading['v']
            
            # Calculate Heat Index
            heat_index_c = calculate_heat_index(t_val, h_val)
            
            print(f"--- Weather Data Parsed ---")
            print(f"Actual Temp: {t_val} °C")
            print(f"Humidity:    {h_val} %")
            print(f"Feels Like:  {heat_index_c:.1f} °C")
            
            # Alert Logic
            if heat_index_c > 40: # approx 104 F
                print("⚠️ DANGER: Extreme Heat Risk")
            elif heat_index_c > 32: # approx 90 F
                print("⚠️ CAUTION: High Heat Risk")
            else:
                print("✅ Status: Normal")
                
        else:
            print("Error: Missing Temperature or Humidity data.")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")

# Run the function
process_heat_index(senml_data)

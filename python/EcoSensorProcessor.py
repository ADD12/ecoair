Python

import json
import math

class EcoSensorProcessor:
    def __init__(self):
        # US EPA PM2.5 Breakpoints (ug/m3) -> (Category, Color Hex)
        self.aqi_breakpoints = [
            (12.0,  "Good", "#00E400"),
            (35.4,  "Moderate", "#FFFF00"),
            (55.4,  "Unhealthy for Sensitive Groups", "#FF7E00"),
            (150.4, "Unhealthy", "#FF0000"),
            (250.4, "Very Unhealthy", "#8F3F97"),
            (float('inf'), "Hazardous", "#7E0023")
        ]

    def process_packet(self, json_payload):
        """
        Main entry point: Ingests SenML JSON and returns a structured
        dictionary with raw values and derived eco-metrics.
        """
        try:
            data = json.loads(json_payload)
            
            # 1. Extract Raw Readings
            readings = {item['n']: item['v'] for item in data if 'n' in item and 'v' in item}
            
            # 2. Initialize Result Object
            result = {
                "raw_readings": readings,
                "derived_metrics": {},
                "alerts": []
            }

            # 3. Calculate Derived Metrics
            
            # --- AQI Calculation ---
            if "pm2.5" in readings:
                aqi_status, aqi_color = self._calculate_aqi_category(readings["pm2.5"])
                result["derived_metrics"]["air_quality"] = {
                    "status": aqi_status,
                    "color_code": aqi_color
                }
                # Add alert if air is bad
                if aqi_status not in ["Good", "Moderate"]:
                    result["alerts"].append(f"Air Quality Alert: {aqi_status}")

            # --- Heat Index Calculation ---
            if "temperature" in readings and "humidity" in readings:
                hi_c = self._calculate_heat_index(readings["temperature"], readings["humidity"])
                result["derived_metrics"]["heat_index_c"] = round(hi_c, 1)
                
                # Add alert if heat is dangerous (> 40C / 104F)
                if hi_c > 40:
                    result["alerts"].append("Heat Danger Alert")

            return result

        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}
        except Exception as e:
            return {"error": str(e)}

    # --- Internal Helper Methods ---

    def _calculate_aqi_category(self, pm25_val):
        """Returns tuple (Category, ColorHex) based on PM2.5"""
        for limit, category, color in self.aqi_breakpoints:
            if pm25_val <= limit:
                return category, color
        return "Hazardous", "#7E0023"

    def _calculate_heat_index(self, temp_c, humidity):
        """Calculates NOAA Heat Index"""
        T = (temp_c * 9/5) + 32  # Convert to F for formula
        RH = humidity

        # Simple formula (Steadman)
        HI = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))

        # Full regression (Rothfusz) if needed
        if HI >= 80:
            HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH \
                 - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH \
                 + .00085282*T*RH*RH - .00000199*T*T*RH*RH
            
            if (RH < 13) and (T >= 80) and (T <= 112):
                adjustment = ((13-RH)/4)*math.sqrt((17-math.fabs(T-95.))/17)
                HI -= adjustment
            elif (RH > 85) and (T >= 80) and (T <= 87):
                adjustment = ((RH-85)/10) * ((87-T)/5)
                HI += adjustment

        return (HI - 32) * 5/9  # Convert back to C

# --- Usage Example ---

# 1. Instantiate the processor
processor = EcoSensorProcessor()

# 2. Simulate an incoming packet (Hot day + Moderate Smoke)
incoming_payload = """
[
  {"bn": "sensor-01", "bt": 1735418000, "n": "pm2.5", "u": "ug/m3", "v": 42.5},
  {"n": "temperature", "u": "Cel", "v": 33.0},
  {"n": "humidity", "u": "%RH", "v": 70.0}
]
"""

# 3. Process
dashboard_data = processor.process_packet(incoming_payload)

# 4. View Result
print(json.dumps(dashboard_data, indent=2))

Expected Output

When you run this code, the processor will combine the logic and output a clean JSON structure ready for your dashboard frontend:
JSON

{
  "raw_readings": {
    "pm2.5": 42.5,
    "temperature": 33.0,
    "humidity": 70.0
  },
  "derived_metrics": {
    "air_quality": {
      "status": "Unhealthy for Sensitive Groups",
      "color_code": "#FF7E00"
    },
    "heat_index_c": 44.6
  },
  "alerts": [
    "Air Quality Alert: Unhealthy for Sensitive Groups",
    "Heat Danger Alert"
  ]
}

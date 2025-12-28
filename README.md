# ecoair-ecodashboard v0.1
and generic Air Quaility App for both indoor and putdoor Air Quaility
nteroperability & API Standards (The "Gold Standard")
These standards define how your dashboard talks to the server or sensor network.
OGC SensorThings API:
What it is: An open standard by the Open Geospatial Consortium (OGC) specifically designed for IoT devices and environmental monitoring.
Why use it: It provides a unified way to manage sensors, locations, and historical readings. It uses standard JSON and is REST-based, making it very easy for web developers to query.
Key Concept: It separates the Thing (the physical device) from the Datastream (the flow of readings), which is critical for complex eco-dashboards.
OpenAQ Data Format:
What it is: While not a formal ISO standard, OpenAQ has become the de facto open standard for aggregating air quality data globally.
Why use it: If you want your dashboard to display public data alongside your private sensors for comparison, following the OpenAQ JSON structure ensures compatibility with the world's largest open air quality dataset.
2. Device-Level Communication Protocols
These are the open standards used by the sensors to send data to your backend.
MQTT (Message Queuing Telemetry Transport):
Status: ISO Standard (ISO/IEC 20922).
Why use it: The industry standard for IoT. It is lightweight and works well over unstable internet connections (common in remote outdoor sensor deployments). Sensors "publish" readings to a topic (e.g., sensors/patio/pm25) that your dashboard "subscribes" to.
CoAP (Constrained Application Protocol):
Status: IETF Standard (RFC 7252).
Why use it: Similar to HTTP but designed for very low-power sensors (battery or solar-powered). If your eco-dashboard relies on remote field sensors with limited power, they will likely use CoAP.
3. Data Payload Standards (The Data Structure)
When the data arrives, it should be formatted in a standard way so your dashboard can parse it.
GeoJSON:
Standard: IETF RFC 7946.
Usage: Essential for map-based dashboards. Instead of just sending a reading {"pm25": 12}, you send a feature that includes the precise location geometry. This allows libraries like Mapbox or Leaflet to instantly render the sensor on a map.
SenML (Sensor Measurement Lists):
Standard: IETF RFC 8428.
Usage: A standard JSON format specifically for simple sensor readings. It looks like this: [{"n":"pm2.5", "u":"ug/m3", "v":12.5}]. It standardizes the names (n), units (u), and values (v), preventing confusion between different sensor brands.
4. Semantic Standards (The "Vocabulary")
To ensure "PM2.5" means the same thing across all devices.
EPA Air Quality Index (AQI) Breakpoints:
While technically a government standard, using the EPA's specific breakpoints for converting raw concentration (µg/m³) into an AQI integer (0-500) and color code (Green/Yellow/Red) is the standard expectation for user-facing dashboards.
Note: If you have an international audience, you may need to support the CAQI (Common Air Quality Index) used in Europe.
Summary Recommendation for Your Stack
If you are building a modern web-based eco-dashboard, I recommend this combination:
Transport: MQTT (for real-time sensor updates).
Data Structure: GeoJSON (to easily plot sensors on a map).
API Style: OGC SensorThings (for querying history and metadata).

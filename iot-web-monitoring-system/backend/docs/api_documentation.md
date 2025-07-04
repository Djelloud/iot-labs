# IoT Backend API Documentation

## Overview

The IoT Backend API provides RESTful endpoints for accessing temperature and humidity sensor data from a DHT11 sensor connected to a Raspberry Pi.

**Base URL**: `http://localhost:8080`

## Authentication

No authentication required (development/academic environment).

## Endpoints

### Temperature Endpoints

#### Get Latest Temperature
```http
GET /capteurs/temp
```

**Description**: Returns the most recent temperature reading.

**Response**:
- **Success (200)**: Returns temperature value as string
- **Error (404)**: "Aucune données de température disponible"

**Example**:
```bash
curl http://localhost:8080/capteurs/temp
# Response: "23.5"
```

#### Get Temperature History
```http
GET /capteurs/temp/:n
```

**Description**: Returns the last n temperature readings with timestamps.

**Parameters**:
- `n` (integer): Number of readings to retrieve (must be positive)

**Response**:
- **Success (200)**: JSON array of [timestamp, temperature] pairs
- **Error (400)**: "Paramètre invalide"

**Example**:
```bash
curl http://localhost:8080/capteurs/temp/5
# Response: [
#   ["2024-12-03 15:30:15", 23.5],
#   ["2024-12-03 15:30:18", 23.6],
#   ["2024-12-03 15:30:21", 23.4],
#   ["2024-12-03 15:30:24", 23.7],
#   ["2024-12-03 15:30:27", 23.5]
# ]
```

#### Get Temperature Average
```http
GET /capteurs/temp/:n/moy
```

**Description**: Returns the average temperature of the last n readings.

**Parameters**:
- `n` (integer): Number of readings to include in average calculation

**Response**:
- **Success (200)**: Average temperature as string
- **Error (400)**: "Paramètre invalide"
- **Error (404)**: "Aucune données de température disponible"

**Example**:
```bash
curl http://localhost:8080/capteurs/temp/10/moy
# Response: "23.6"
```

### Humidity Endpoints

#### Get Latest Humidity
```http
GET /capteurs/hum
```

**Description**: Returns the most recent humidity reading.

**Response**:
- **Success (200)**: Returns humidity value as string with % symbol
- **Error (404)**: "Aucune données d'humidité disponible"

**Example**:
```bash
curl http://localhost:8080/capteurs/hum
# Response: "65.2%"
```

#### Get Humidity History
```http
GET /capteurs/hum/:n
```

**Description**: Returns the last n humidity readings with timestamps.

**Parameters**:
- `n` (integer): Number of readings to retrieve (must be positive)

**Response**:
- **Success (200)**: JSON array of [timestamp, humidity] pairs
- **Error (400)**: "Paramètre invalide"

**Example**:
```bash
curl http://localhost:8080/capteurs/hum/3
# Response: [
#   ["2024-12-03 15:30:24", 65.2],
#   ["2024-12-03 15:30:27", 65.1],
#   ["2024-12-03 15:30:30", 65.3]
# ]
```

#### Get Humidity Average
```http
GET /capteurs/hum/:n/moy
```

**Description**: Returns the average humidity of the last n readings.

**Parameters**:
- `n` (integer): Number of readings to include in average calculation

**Response**:
- **Success (200)**: Average humidity as string with % symbol
- **Error (400)**: "Paramètre invalide"
- **Error (404)**: "Aucune données d'humidité disponible"

**Example**:
```bash
curl http://localhost:8080/capteurs/hum/5/moy
# Response: "65.1%"
```

## Data Format

### Timestamp Format
All timestamps are in ISO format: `YYYY-MM-DD HH:MM:SS`

### Temperature Values
- Unit: Celsius (°C)
- Precision: 1 decimal place
- Range: Typically -40°C to 80°C (DHT11 sensor limits)

### Humidity Values
- Unit: Percentage (%)
- Precision: 1 decimal place
- Range: 0% to 100%

## Error Handling

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameter)
- `404`: Not Found (no data available)
- `500`: Internal Server Error

### Error Response Format
```json
{
  "error": "Error message in French"
}
```

## Rate Limiting

No rate limiting implemented in current version.

## CORS Policy

CORS is enabled for all origins (`*`) to allow frontend access.

## Data Storage

- **Storage Type**: In-memory
- **Max History**: 720 readings (configurable)
- **Reading Interval**: 3 seconds
- **Data Retention**: Approximately 1 hour at current settings

## Sensor Configuration

- **Sensor Type**: DHT11
- **GPIO Pin**: 17
- **Library**: node-dht-sensor

## Testing Examples

### Complete Test Suite
```bash
# Test latest readings
curl http://localhost:8080/capteurs/temp
curl http://localhost:8080/capteurs/hum

# Test history (last 10 readings)
curl http://localhost:8080/capteurs/temp/10
curl http://localhost:8080/capteurs/hum/10

# Test averages
curl http://localhost:8080/capteurs/temp/30/moy
curl http://localhost:8080/capteurs/hum/30/moy

# Test error cases
curl http://localhost:8080/capteurs/temp/0      # Should return 400
curl http://localhost:8080/capteurs/temp/abc    # Should return 400
```

## Notes

- The server must be running on a Raspberry Pi with a connected DHT11 sensor for live data
- In testing environments without hardware, the API will return 404 errors
- All French error messages are intentional for the academic context

---
*API Version: 1.0.0*
*Last updated: December 2024* 
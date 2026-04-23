# API Reference

LumeHaven provides a RESTful API for controlling and monitoring the server. The API uses standard HTTP methods and returns JSON responses.

**Base URL:** `http://localhost:5000` (or your configured host/port)

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/status` | Check server status |
| POST | `/start` | Start game monitoring |
| POST | `/stop` | Stop game monitoring |
| GET | `/scenes` | List all available scenes |
| GET | `/scenes/current` | Get current active scene |
| POST | `/scenes/<scene_name>` | Set active scene |
| GET | `/lamps` | List all configured lamps |
| GET | `/lamps/<entity_id>` | Get lamp configuration |
| POST | `/lamps/<entity_id>/color` | Set lamp color |
| POST | `/lamps/<entity_id>/brightness` | Set lamp brightness |

## Detailed Endpoints

### Server Management

#### GET /status

Check if the LumeHaven server is running and whether game monitoring is active.

**Request:**
```bash
curl http://localhost:5000/status
```

**Response:**
```json
{
  "started": false
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `started` | boolean | `true` if the game monitoring loop is running, `false` otherwise |

**Status Codes:**
- `200 OK` - Success

---

#### POST /start

Start the game monitoring loop. LumeHaven will begin polling the GHS database for changes and triggering lighting effects.

**Request:**
```bash
curl -X POST http://localhost:5000/start
```

**Response:**
```
ok
```

**Status Codes:**
- `200 OK` - Game monitoring started successfully

**Notes:**
- If monitoring is already running, this has no effect
- Use `/status` to verify the monitoring is active

---

#### POST /stop

Stop the game monitoring loop. LumeHaven will stop checking for game state changes.

**Request:**
```bash
curl -X POST http://localhost:5000/stop
```

**Response:**
```
ok
```

**Status Codes:**
- `200 OK` - Game monitoring stopped successfully

**Notes:**
- If monitoring is already stopped, this has no effect
- Lamps will retain their last state

---

### Scene Management

#### GET /scenes

List all available scenes defined in the configuration.

**Request:**
```bash
curl http://localhost:5000/scenes
```

**Response:**
```json
[
  "tavern",
  "dungeon",
  "forest",
  "frost",
  "victory"
]
```

**Response:** Array of scene names as strings

**Status Codes:**
- `200 OK` - Success

---

#### GET /scenes/current

Get the currently active scene name.

**Request:**
```bash
curl http://localhost:5000/scenes/current
```

**Response:**
```json
"tavern"
```

**Response:** Scene name as a string, or `"none"` if no scene is active

**Status Codes:**
- `200 OK` - Scene is active
- `404 Not Found` - No scene is currently active

---

#### POST /scenes/<scene_name>

Activate a specific scene. All lamps will cycle through the scene's colors.

**Request:**
```bash
curl -X POST http://localhost:5000/scenes/dungeon
```

**Response:**
```
ok
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scene_name` | string | Yes | Name of the scene to activate. Must match a scene defined in `config.yml` |

**Status Codes:**
- `200 OK` - Scene activated successfully
- `404 Not Found` - Scene with the specified name does not exist

**Example Error Response:**
```
No scene named: non_existent_scene
```

---

### Lamp Management

#### GET /lamps

List all configured lamps and their configuration.

**Request:**
```bash
curl http://localhost:5000/lamps
```

**Response:**
```json
[
  {
    "type": "yeelight",
    "id": "living-room-lamp",
    "ip": "192.168.0.42"
  },
  {
    "type": "logging_lamp",
    "id": "debug-lamp"
  }
]
```

**Response:** Array of lamp configuration objects

**Lamp Object Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Lamp integration type (e.g., `yeelight`, `logging_lamp`) |
| `id` | string | Unique identifier for the lamp |
| `ip` | string | IP address of the lamp (if applicable) |
| Additional fields | varies | Any integration-specific configuration |

**Status Codes:**
- `200 OK` - Success

---

#### GET /lamps/<entity_id>

Get the configuration for a specific lamp.

**Request:**
```bash
curl http://localhost:5000/lamps/living-room-lamp
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `entity_id` | string | Yes | The `id` of the lamp as defined in `config.yml` |

**Response:**
```json
{
  "type": "yeelight",
  "id": "living-room-lamp",
  "ip": "192.168.0.42"
}
```

**Status Codes:**
- `200 OK` - Lamp found and configuration returned
- `404 Not Found` - No lamp with the specified `entity_id` exists

**Example Error Response:**
```
ValueError: No lamp for given entity id: unknown-lamp
```

---

#### POST /lamps/<entity_id>/color

Set the color of a specific lamp immediately.

**Request:**
```bash
curl -X POST http://localhost:5000/lamps/living-room-lamp/color \
  -H "Content-Type: application/json" \
  -d '{"r": 255, "g": 0, "b": 0}'
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `entity_id` | string | Yes | The `id` of the lamp to control |

**Request Body:**
```json
{
  "r": 255,
  "g": 0,
  "b": 0
}
```

**Request Body Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `r` | integer | Yes | Red component (0-255) |
| `g` | integer | Yes | Green component (0-255) |
| `b` | integer | Yes | Blue component (0-255) |

**Response:**
```
ok
```

**Status Codes:**
- `200 OK` - Color set successfully
- `404 Not Found` - No lamp with the specified `entity_id` exists

---

#### POST /lamps/<entity_id>/brightness

Set the brightness of a specific lamp.

**Request:**
```bash
curl -X POST http://localhost:5000/lamps/living-room-lamp/brightness \
  -H "Content-Type: text/plain" \
  -d '50'
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `entity_id` | string | Yes | The `id` of the lamp to control |

**Request Body:**
Raw integer value (0-100) as plain text

| Type | Description |
|------|-------------|
| integer | Brightness percentage (0-100 where 100 is full brightness) |

**Response:**
```
ok
```

**Status Codes:**
- `200 OK` - Brightness set successfully
- `404 Not Found` - No lamp with the specified `entity_id` exists

## Usage Examples

### Complete Session Example

```bash
# Start LumeHaven server (in one terminal)
python -m lumehaven

# In another terminal:

# Check server status
curl http://localhost:5000/status
# {"started": false}

# Start game monitoring
curl -X POST http://localhost:5000/start

# List available scenes
curl http://localhost:5000/scenes
# ["tavern", "dungeon", "forest"]

# Set a specific scene
curl -X POST http://localhost:5000/scenes/dungeon

# List configured lamps
curl http://localhost:5000/lamps
# [{"type": "yeelight", "id": "living-room-lamp", "ip": "192.168.0.42"}]

# Set lamp color directly
curl -X POST http://localhost:5000/lamps/living-room-lamp/color \
  -H "Content-Type: application/json" \
  -d '{"r": 0, "g": 255, "b": 0}'

# Set lamp brightness
curl -X POST http://localhost:5000/lamps/living-room-lamp/brightness \
  -d '75'

# Get current scene
curl http://localhost:5000/scenes/current
# "dungeon"

# Stop game monitoring
curl -X POST http://localhost:5000/stop

# Check final status
curl http://localhost:5000/status
# {"started": false}
```

### Using with Python

```python
import requests

BASE_URL = "http://localhost:5000"

# Start monitoring
response = requests.post(f"{BASE_URL}/start")
print(response.text)  # ok

# Set scene
response = requests.post(f"{BASE_URL}/scenes/forest")
print(response.status_code)  # 200

# List lamps
response = requests.get(f"{BASE_URL}/lamps")
lamps = response.json()
print(lamps)

# Set color for first lamp
if lamps:
    lamp_id = lamps[0]['id']
    color = {"r": 255, "g": 100, "b": 0}
    response = requests.post(f"{BASE_URL}/lamps/{lamp_id}/color", json=color)
    print(response.text)  # ok

# Get current scene
response = requests.get(f"{BASE_URL}/scenes/current")
print(f"Current scene: {response.json()}")

# Stop monitoring
response = requests.post(f"{BASE_URL}/stop")
```

### Using with Home Assistant (RESTful Command)

You can integrate LumeHaven with Home Assistant using RESTful commands:

```yaml
# configuration.yaml
rest_command:
  lumehaven_start:
    url: "http://localhost:5000/start"
    method: POST
  lumehaven_stop:
    url: "http://localhost:5000/stop"
    method: POST
  lumehaven_scene:
    url: "http://localhost:5000/scenes/{{ scene }}"
    method: POST

# automation.yaml
automation:
  - alias: "Start LumeHaven when Gloomhaven starts"
    trigger:
      - platform: state
        entity_id: input_boolean.gloomhaven_session
        to: "on"
    action:
      - service: rest_command.lumehaven_start

  - alias: "Set LumeHaven scene"
    trigger:
      - platform: state
        entity_id: input_select游戏场景
        to: "dungeon"
    action:
      - service: rest_command.lumehaven_scene
        data:
          scene: "dungeon"
```

## API Integration with Other Tools

The LumeHaven API can be used with various tools and platforms:

### Node-RED

Create flows that trigger LumeHaven actions based on external events.

### IFTTT / Zapier

Use webhook integrations to trigger LumeHaven from external services.

### Custom Scripts

Write scripts in any language to control LumeHaven programmatically.

### Stream Deck

Create Stream Deck buttons that trigger scene changes or control lamps.

## Error Handling

The API provides appropriate HTTP status codes and error messages:

| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Success | `ok` or JSON data |
| `404 Not Found` | Resource not found | Error message string |
| `400 Bad Request` | Invalid request | Error description |
| `500 Internal Server Error` | Server error | Error details |

### Common Errors

**Lamp not found:**
```bash
curl http://localhost:5000/lamps/nonexistent
# ValueError: No lamp for given entity id: nonexistent
```

**Scene not found:**
```bash
curl -X POST http://localhost:5000/scenes/nonexistent
# No scene named: nonexistent
```

**Invalid color values:**
```bash
# RGB values must be 0-255
curl -X POST http://localhost:5000/lamps/mylamp/color \
  -d '{"r": 300, "g": 0, "b": 0}'
# pydantic.error_wrappers.ValidationError
```

## Rate Limiting and Performance

- The API has no built-in rate limiting
- For production use, consider adding a reverse proxy (nginx, Apache) with rate limiting
- Lamp operations are performed in real-time and may have latency depending on:
  - Network speed
  - Lamp response time
  - Current lamp state

## Security

**Important:** The LumeHaven API currently does not include authentication. For safe usage:

1. **Run on local network only** - Do not expose to the internet
2. **Use firewall rules** - Restrict access to trusted IPs
3. **Add a reverse proxy** - Use nginx/Apache with authentication
4. **Use VPN** - For remote access, use a VPN instead of exposing directly

### Adding Authentication (Future)

For future implementations, consider adding:
- API key authentication
- JWT tokens
- OAuth2

## API Versioning

The current API is version 1. Backward compatibility is maintained within major versions.

## Changelog

### v1.0

Initial API version with:
- Server management endpoints
- Scene management endpoints
- Lamp management endpoints

## See Also

- [Quick Start](quick-start.md) - Get LumeHaven running
- [Setup Guide](setup-guide.md) - Detailed setup instructions
- [Configuration](configuration.md) - Configure scenes, lamps, and effects
- [Integrations](integrations.md) - Create custom lamp integrations
- [Events & Effects](events-and-effects.md) - Available game events

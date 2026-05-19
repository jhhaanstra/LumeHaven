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

## See Also

- [Quick Start](quick-start.md) - Get LumeHaven running
- [Configuration](configuration.md) - Configure scenes, lamps, and effects
- [Integrations](integrations.md) - Create custom lamp integrations
- [Events & Effects](events-and-effects.md) - Available game events

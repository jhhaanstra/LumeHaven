# Lamp Integrations Guide

LumeHaven uses a plugin-based architecture for lamp integrations. This allows you to add support for any smart lighting system. This guide explains how integrations work and how to create your own.

## How Integrations Work

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      LumeHaven Core                             │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │  LampService     │    │  Event System    │                   │
│  │  - Manages lamps │    │  - Game events   │                   │
│  │  - Handles scenes│    │  - Light effects │                   │
│  └──────────────────┘    └──────────────────┘                   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Lamp Abstract Interface                                │    │
│  │  - turn_color(RGB)                                      │    │
│  │  - set_brightness(int)                                  │    │
│  │  - pulse(RGB)                                           │    │
│  │  - cycle(list[RGB])                                     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Lamp Provider Plugins                         │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │  YeelightLamp   │    │  LoggingLamp    │      ┌───────────┐  │
│  │  (yeelight.py)  │    │  (logging.py)   │      │  YourLamp │  │
│  └─────────────────┘    └─────────────────┘      │  (custom) │  │
│                                                  └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Physical/Virtual Lamps                      │
│  Yeelight Bulbs | Philips Hue | LIFX | Home Assistant | etc.    │
└─────────────────────────────────────────────────────────────────┘
```

### Plugin Discovery

LumeHaven discovers lamp providers using Python's **entry points** system. When LumeHaven starts, it:

1. Scans for entry points under the group `lumehaven.lamp_providers`
2. Loads each entry point as a lamp factory function
3. Registers the factory with the lamp type name

This is defined in `pyproject.toml`:

```toml
[project.entry-patterns."lumehaven.lamp_providers"]
logging_lamp = "lamp_integrations.logging_lamp:create_logging_lamp"
yeelight = "lamp_integrations.yeelight:create_yeelight_lamp"
```

## Creating a Lamp Integration

All lamp integrations must implement the `Lamp` abstract base class in `lumehaven/lights/lamps.py`.
To create a new lamp integration, follow these steps:

### Step 1: Create the Lamp Class

Create a new Python file in the `src/lamp_integrations/` directory (or any Python package that's importable).

Example: `src/lamp_integrations/my_custom_lamp_file.py`

```python
from typing import Optional

from lumehaven.core.config import LampConfig
from lumehaven.lights.lamps import RGB, Lamp


class CustomLamp(Lamp):

    ...

    def turn_color(self, rgb: RGB):
        # Communicate with lamp to switch to provided color
        ...

    def set_brightness(self, brightness: int):
        # Communicate with lamp to set provided brightness
        ...

    def pulse(self, rgb: RGB):
        # Pulse lamp by either using a dedicated command or by using the turn_color a couple of times
        ...

    def cycle(self, rgb_flow: list[RGB]):
        # Cycle through colors
        ...
```

### Step 2: Create a Factory Function

LumeHaven expects a factory function that creates lamp instances based on configuration.

```python
def create_custom_lamp(config: LampConfig) -> Optional[Lamp]:
    if config.type != "custom_lamp":
        return None

    # Extract configuration specific to Philips Hue
    light_id = config.light_id  # Custom field in config
    
    return PhilipsHueLamp(
        entity_id=config.id,
        ip=config.ip,
        light_id=light_id
    )
```

### Step 3: Register the Entry Point

Add the factory function to `pyproject.toml`:

```toml
[project.entry-points."lumehaven.lamp_providers"]
logging_lamp = "lamp_integrations.logging_lamp:create_logging_lamp"
yeelight = "lamp_integrations.yeelight:create_yeelight_lamp"
custom_lamp = "lamp_integrations.my_custom_lamp_file:create_custom_lamp"
```

### Step 4: Add Dependencies

In case your lamp uses an external dependency, like the Yeelight lamps, don't forget to add any required dependencies to `pyproject.toml`:

```toml
[project.dependencies]
# ... existing dependencies ...
```

### Step 5: Update Configuration

Now you can use your new lamp type in `config.yml`:

```yaml
lamps:
  - type: "custom_lamp"
    id: "custom-lamp-1"
    ip: "192.168.0.50"
```

## Existing Integrations

### Yeelight Integration

The Yeelight integration (`src/lamp_integrations/yeelight.py`) demonstrates a complete implementation:

**Dependencies:**
- `yeelight>=0.7.16`

**Configuration:**
```yaml
lamps:
  - type: "yeelight"
    id: "my-lamp"
    ip: "192.168.0.42"
```

### Logging Lamp Integration

The logging lamp (`src/lamp_integrations/logging_lamp.py`) is a simple integration for debugging:

**Configuration:**
```yaml
lamps:
  - type: "logging_lamp"
    id: "debug"
```

## Lamp Configuration

The `LampConfig` class (`src/lumehaven/core/config.py`) defines the configuration schema for lamps:

```python
class LampConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    type: str
    id: str
    ip: str
    
    def dict(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(**kwargs)
```

**Notes:**
- The `type` field must match the entry point name
- The `id` field is a unique identifier within LumeHaven
- The `ip` field is the network address of the lamp

## Testing Your Integration

### Manual Testing

1. Update `config.yml` with your lamp configuration
2. Start LumeHaven:
   ```bash
   python -m lumehaven
   ```
3. Check logs for plugin loading:
   ```
   INFO - Found integration type: philips_hue
   ```
4. Use the API to test:
   ```bash
   # Set color
   curl -X POST http://localhost:5000/lamps/my-lamp/color -H "Content-Type: application/json" -d '{"r": 255, "g": 0, "b": 0}'
   
   # Trigger pulse
   curl -X POST http://localhost:5000/start
   # Then trigger a game event in GHS
   ```

## Packaging and Distribution

### Local Development

1. Install in development mode:
   ```bash
   pip install -e .
   # or
   uv sync
   ```

2. Test your integration:
   ```bash
   python -m lumehaven
   ```

## See Also

- [Configuration Reference](configuration.md) - How to configure lamps
- [API Reference](api-reference.md) - Test integrations via API
- [Events & Effects](events-and-effects.md) - Available game events
- [GitHub: yeelight Python library](https://github.com/shenxn/yeelight)
- [Home Assistant Integrations](https://www.home-assistant.io/integrations/)

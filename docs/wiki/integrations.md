# Lamp Integrations Guide

LumeHaven uses a plugin-based architecture for lamp integrations. This allows you to add support for any smart lighting system. This guide explains how integrations work and how to create your own.

## How Integrations Work

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      LumeHaven Core                               │
│  ┌─────────────────┐    ┌─────────────────┐                      │
│  │  LampService     │    │  Event System    │                      │
│  │  - Manages lamps │    │  - Game events   │                      │
│  │  - Handles scenes│    │  - Light effects │                      │
│  └─────────────────┘    └─────────────────┘                      │
│                           │                                         │
│                           ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Lamp Abstract Interface                              │    │
│  │  - turn_color(RGB)                                    │    │
│  │  - set_brightness(int)                               │    │
│  │  - pulse(RGB)                                        │    │
│  │  - cycle(list[RGB])                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Lamp Provider Plugins                           │
│  ┌─────────────────┐    ┌─────────────────┐                      │
│  │  YeelightLamp    │    │  LoggingLamp     │      ┌───────────┐   │
│  │  (yeelight.py)   │    │  (logging.py)    │      │  YourLamp  │   │
│  └─────────────────┘    └─────────────────┘      │  (custom)   │   │
│                                              └───────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Physical/Virtual Lamps                         │
│  Yeelight Bulbs | Philips Hue | LIFX | Home Assistant | etc.       │
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

## Lamp Interface

All lamp integrations must implement the `Lamp` abstract base class:

### Base Lamp Class (`lumehaven/lights/lamps.py`)

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel

class RGB(BaseModel):
    r: int
    g: int
    b: int

    def as_list(self):
        return [self.r, self.g, self.b]


class Lamp(ABC):
    @abstractmethod
    def turn_color(self, rgb: RGB):
        """Set the lamp to a specific color immediately."""
        pass

    @abstractmethod
    def set_brightness(self, brightness: int):
        """Set the lamp's brightness (0-100)."""
        pass

    @abstractmethod
    def pulse(self, rgb: RGB):
        """Pulse the lamp with the specified color (quick flash)."""
        pass

    @abstractmethod
    def cycle(self, rgb_flow: list[RGB]):
        """Cycle through a list of colors smoothly."""
        pass
```

### Method Descriptions

| Method | Parameters | Description |
|--------|------------|-------------|
| `turn_color` | `rgb: RGB` | Immediately set the lamp to the specified RGB color |
| `set_brightness` | `brightness: int` | Set brightness level (0-100 where 100 is full brightness) |
| `pulse` | `rgb: RGB` | Create a pulse/flash effect with the specified color |
| `cycle` | `rgb_flow: list[RGB]` | Smoothly cycle through a list of colors in a loop |

## Creating a Lamp Integration

To create a new lamp integration, follow these steps:

### Step 1: Create the Lamp Class

Create a new Python file in the `src/lamp_integrations/` directory (or any Python package that's importable).

Example: `src/lamp_integrations/philips_hue.py`

```python
from typing import Optional

from lumehaven.core.config import LampConfig
from lumehaven.lights.lamps import RGB, Lamp


class PhilipsHueLamp(Lamp):
    """
    Controls Philips Hue lights via the Hue API.
    Requires the qhue library: pip install qhue
    """

    def __init__(self, entity_id: str, ip: str, light_id: int):
        from qhue import Qhue
        self.entity_id = entity_id
        self.ip = ip
        self.light_id = light_id
        self.bridge = Qhue(ip)

    def turn_color(self, rgb: RGB):
        # Convert RGB to Hue color space and send to bridge
        self.bridge.set_light(self.light_id, {'rgb': (rgb.r, rgb.g, rgb.b)})

    def set_brightness(self, brightness: int):
        # Hue uses 0-255 for brightness
        hue_brightness = int((brightness / 100) * 255)
        self.bridge.set_light(self.light_id, {'bri': hue_brightness})

    def pulse(self, rgb: RGB):
        # Create a pulse effect
        # Save current color
        current = self.bridge.get_light(self.light_id)
        
        # Set to pulse color
        self.turn_color(rgb)
        
        # Wait briefly (simplified - real implementation would use async)
        import time
        time.sleep(0.5)
        
        # Restore original color
        self.bridge.set_light(self.light_id, {'rgb': current['rgb']})

    def cycle(self, rgb_flow: list[RGB]):
        # Cycle through colors
        import time
        for color in rgb_flow:
            self.turn_color(color)
            time.sleep(1)  # Adjust duration as needed
            
        # Loop back to first color
        self.cycle(rgb_flow)
```

### Step 2: Create a Factory Function

LumeHaven expects a factory function that creates lamp instances based on configuration.

```python
def create_philips_hue_lamp(config: LampConfig) -> Optional[Lamp]:
    """
    Factory function for Philips Hue lamp.
    
    Args:
        config: LampConfig from YAML configuration
        
    Returns:
        PhilipsHueLamp instance or None if config type doesn't match
    """
    if config.type != "philips_hue":
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
philips_hue = "lamp_integrations.philips_hue:create_philips_hue_lamp"
```

### Step 4: Add Dependencies

Add any required dependencies to `pyproject.toml`:

```toml
[project.dependencies]
# ... existing dependencies ...
"qhue>=1.0.0"  # For Philips Hue support
```

Or as optional dependencies:

```toml
[project.optional-dependencies]
philips_hue = ["qhue>=1.0.0"]
```

### Step 5: Update Configuration

Now you can use your new lamp type in `config.yml`:

```yaml
lamps:
  - type: "philips_hue"
    id: "hue-light-1"
    ip: "192.168.0.50"
    light_id: 1  # Philips Hue light ID
```

## Existing Integrations

### Yeelight Integration

The Yeelight integration (`src/lamp_integrations/yeelight.py`) demonstrates a complete implementation:

```python
from typing import Optional
from yeelight import Bulb, Flow, RGBTransition

from lumehaven.core.config import LampConfig
from lumehaven.lights.lamps import RGB, Lamp


def create_yeelight_lamp(config: LampConfig) -> Optional[Lamp]:
    if config.type != "yeelight":
        return None

    return YeeLightLamp(config.id, config.ip)


class YeeLightLamp(Lamp):
    def __init__(self, entity_id: str, ip: str):
        self.bulb = Bulb(ip)
        self.entity_id = entity_id
        self.ip = ip

    def turn_color(self, rgb: RGB):
        self.bulb.set_rgb(rgb.r, rgb.g, rgb.b)

    def set_brightness(self, brightness: int):
        # Yeelight uses 1-100 for brightness
        self.bulb.set_brightness(brightness)

    def pulse(self, rgb: RGB):
        transitions = [RGBTransition(rgb.r, rgb.g, rgb.b, duration=300)]
        flow = Flow(count=2, transitions=transitions)
        self.bulb.start_flow(flow)

    def cycle(self, rgb_flow: list[RGB]):
        flow = Flow(
            count=0,  # 0 means infinite loop
            transitions=list(
                map(
                    lambda rgb: RGBTransition(rgb.r, rgb.g, rgb.b, duration=3000),
                    rgb_flow,
                )
            ),
        )
        self.bulb.start_flow(flow)
```

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

```python
from typing import Optional

from lumehaven.core.config import LampConfig
from lumehaven.lights.lamps import RGB, Lamp


def create_logging_lamp(config: LampConfig) -> Optional[Lamp]:
    if config.type != "logging_lamp":
        return None
    return LoggingLamp()


class LoggingLamp(Lamp):
    def turn_color(self, rgb: RGB):
        print(f"Turning color {rgb}")

    def set_brightness(self, brightness: int):
        print(f"Setting brightness {brightness}")

    def pulse(self, rgb: RGB):
        print(f"Pulsing: {rgb}")

    def cycle(self, rgb_flow: list[RGB]):
        print(f"cycling: {rgb_flow}")
```

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
- `model_config = ConfigDict(extra="allow")` allows additional fields to be passed through
- This enables integration-specific configuration (like `light_id` for Philips Hue)
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

### Unit Testing

Create tests in `tests/lamp_integrations/`:

```python
from lumehaven.core.config import LampConfig
from lumehaven.lights.lamps import RGB
from lamp_integrations.philips_hue import create_philips_hue_lamp, PhilipsHueLamp


def test_create_philips_hue_lamp():
    config = LampConfig(type="philips_hue", id="test", ip="192.168.0.1", light_id=1)
    lamp = create_philips_hue_lamp(config)
    assert isinstance(lamp, PhilipsHueLamp)


def test_philips_hue_turn_color():
    config = LampConfig(type="philips_hue", id="test", ip="192.168.0.1", light_id=1)
    lamp = create_philips_hue_lamp(config)
    # Mock the bridge or use a test double
    # lamp.turn_color(RGB(r=255, g=0, b=0))
    # Verify color was set
```

## Integration Patterns

### Pattern 1: Direct API Access

Some smart light systems have their own APIs (Philips Hue, LIFX, etc.). Use their official SDKs:

```python
import pylifx  # For LIFX
from qhue import Qhue  # For Philips Hue

class LIFX Lamp(Lamp):
    def __init__(self, ip: str):
        self.light = pylifx.Light(ip)
```

### Pattern 2: MQTT Integration

For systems that use MQTT (many Home Assistant setups):

```python
import paho.mqtt.client as mqtt

class MQTTLamp(Lamp):
    def __init__(self, entity_id: str, mqtt_broker: str, topic: str):
        self.client = mqtt.Client()
        self.client.connect(mqtt_broker)
        self.topic = topic
        self.entity_id = entity_id
    
    def turn_color(self, rgb: RGB):
        payload = json.dumps({"color": [rgb.r, rgb.g, rgb.b]})
        self.client.publish(f"{self.topic}/color", payload)
```

**Configuration:**
```yaml
lamps:
  - type: "mqtt"
    id: "ha-living-room"
    mqtt_broker: "192.168.0.100"
    topic: "homeassistant/light/living_room"
```

### Pattern 3: Home Assistant REST API

For controlling Home Assistant entities directly:

```python
import requests

class HomeAssistantLamp(Lamp):
    def __init__(self, entity_id: str, ha_url: str, token: str):
        self.entity_id = entity_id
        self.ha_url = ha_url
        self.token = token
    
    def turn_color(self, rgb: RGB):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        Hex Color
        hex_color = f"#{rgb.r:02x}{rgb.g:02x}{rgb.b:02x}"
        data = {
            "entity_id": self.entity_id,
            "color_name": hex_color
        }
        requests.post(f"{self.ha_url}/api/services/light/turn_on", 
                     headers=headers, json=data)
```

**Configuration:**
```yaml
lamps:
  - type: "homeassistant"
    id: "light.living_room_main"
    ha_url: "http://192.168.0.100:8123"
    token: "your-long-lived-token"
```

### Pattern 4: Virtual/Group Lamps

Create a lamp that controls multiple physical lamps as one:

```python
class GroupLamp(Lamp):
    def __init__(self, entity_id: str, lamps: list[Lamp]):
        self.lamps = lamps
        self.entity_id = entity_id
    
    def turn_color(self, rgb: RGB):
        for lamp in self.lamps:
            lamp.turn_color(rgb)
```

**Configuration:**
```yaml
lamps:
  - type: "group"
    id: "all-lights"
    members: ["lamp1", "lamp2", "lamp3"]
```

## Best Practices for Integration Development

### 1. Error Handling

```python
def turn_color(self, rgb: RGB):
    try:
        self.bulb.set_rgb(rgb.r, rgb.g, rgb.b)
    except Exception as e:
        logging.error(f"Failed to set color on {self.entity_id}: {e}")
        # Optionally: Retry or fallback to a default state
```

### 2. Connection Management

```python
class NetworkLamp(Lamp):
    def __init__(self, entity_id: str, ip: str):
        self.entity_id = entity_id
        self.ip = ip
        self.connected = False
        self._reconnect()
    
    def _reconnect(self):
        try:
            self.connection = self._create_connection()
            self.connected = True
        except Exception as e:
            logging.warning(f"Connection failed for {self.entity_id}: {e}")
            self.connected = False
    
    def turn_color(self, rgb: RGB):
        if not self.connected:
            self._reconnect()
        if self.connected:
            # Set color
        else:
            logging.error(f"Cannot set color: not connected to {self.entity_id}")
```

### 3. Caching and Optimization

```python
class CachedLamp(Lamp):
    def __init__(self, ...):
        self._last_color = None
        self._last_brightness = None
    
    def turn_color(self, rgb: RGB):
        # Only send update if color changed
        if self._last_color != (rgb.r, rgb.g, rgb.b):
            self._do_turn_color(rgb)
            self._last_color = (rgb.r, rgb.g, rgb.b)
```

### 4. Async Support

For integrations that support async operations:

```python
import asyncio

class AsyncLamp(Lamp):
    async def turn_color_async(self, rgb: RGB):
        # Async implementation
        pass
    
    def turn_color(self, rgb: RGB):
        # Run async code synchronously
        asyncio.run(self.turn_color_async(rgb))
```

### 5. Discovery Support

Add device discovery to make setup easier:

```python
class DiscoverableLamp(Lamp):
    @staticmethod
    def discover(timeout: int = 5) -> list[Lamp]:
        """Discover lamps on the network."""
        # Use integration's discovery protocol
        # Return list of LampConfig objects or Lamp instances
        pass
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

### Creating a Package

If you want to distribute your integration separately:

1. Create a new package:
   ```
   lumehaven-philips-hue/
   ├── pyproject.toml
   ├── src/
   │   └── lumehaven_philips_hue/
   │       ├── __init__.py
   │       └── philips_hue.py
   └── README.md
   ```

2. In `pyproject.toml`:
   ```toml
   [project]
   name = "lumehaven-philips-hue"
   dependencies = ["lumehaven", "qhue"]
   
   [project.entry-points."lumehaven.lamp_providers"]
   philips_hue = "lumehaven_philips_hue.philips_hue:create_philips_hue_lamp"
   ```

3. Users can install it:
   ```bash
   pip install lumehaven-philips-hue
   ```

## Troubleshooting Integrations

### Common Issues

**Plugin not loading:**
- Check entry point is registered in `pyproject.toml`
- Verify the package is installed (not just in development mode)
- Check for typos in the entry point name

**Lamp not connecting:**
- Verify IP address and network connectivity
- Check firewall settings
- Test with the `logging_lamp` type to verify LumeHaven is working

**Effects not appearing:**
- Check LumeHaven logs for errors
- Verify lamp is properly initialized
- Test with direct API calls

**Performance issues:**
- Reduce `interval_ms` for faster response (but more CPU)
- Add caching to prevent redundant API calls
- Use async operations where possible

## See Also

- [Configuration Reference](configuration.md) - How to configure lamps
- [API Reference](api-reference.md) - Test integrations via API
- [Events & Effects](events-and-effects.md) - Available game events
- [GitHub: yeelight Python library](https://github.com/shenxn/yeelight)
- [Home Assistant Integrations](https://www.home-assistant.io/integrations/)

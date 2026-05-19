# Events & Effects

LumeHaven reacts to in-game events by triggering lighting effects. This document explains the available events, how to configure effects, and how the event system works.

## Event System Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                        GHS Database                                │
│  Stores game state (characters, monsters, elements, scenario, etc.)│
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                     GameStateFetcher                               │
│  - Polls the SQLite database at configured intervals               │
│  - Retrieves current game state                                    │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                   DbReadingEventPublisher                          │
│  - Compares old state with new state                               │
│  - Checks conditions against game events                           │
│  - Queues matching events                                          │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                       Event Queue                                  │
│  - PulseEvent, SceneEvent, etc.                                    │
└────────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────┐         ┌────────────────────────┐
│    LampService      │         │   Other Subscribers    │
│  - Receives events  │         │  (future extensibility)│
│  - Applies effects  │         └────────────────────────┘
│  - Updates lamps    │
└─────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────────────────────────┐
│                        Physical Lamps                              │
│  - Color changes, pulses, cycles                                   │
└────────────────────────────────────────────────────────────────────┘
```

## Available Events

LumeHaven tracks state changes and triggers events based on differences between polling intervals. All events are triggered when the game state changes from one value to another.

### Element Events

These events trigger when elements on the Gloomhaven element board change state.

| Event ID | Description | Trigger Condition |
|----------|-------------|-------------------|
| `fire_element_active` | Fire element becomes active | Element was inactive, now active (state: 0 -> 1 or 0 -> 2) |
| `ice_element_active` | Ice element becomes active | Element was inactive, now active |
| `air_element_active` | Air element becomes active | Element was inactive, now active |
| `earth_element_active` | Earth element becomes active | Element was inactive, now active |
| `light_element_active` | Light element becomes active | Element was inactive, now active |
| `dark_element_active` | Dark element becomes active | Element was inactive, now active |

**Element States:**
- `0` = Inactive/Waning Double (not active)
- `1` = Waning (weakly active)
- `2` = Strong (strongly active)

**Note:** Only the transition from inactive (0) to active (1 or 2) triggers the event.

### Combat Events

Events related to combat and damage.

| Event ID | Description | Trigger Condition |
|----------|-------------|-------------------|
| `monster_spawned` | A new monster appears | A monster present in new state that wasn't in old state |
| `monster_died` | A monster is defeated | A monster present in old state but not in new state |
| `monster_received_damage` | A monster takes damage | Monster's current health decreased from old to new state |
| `character_died` | A character is exhausted | Character's exhausted state changed from false to true |
| `Character_received_damage` | A character takes damage | Character's current health decreased from old to new state |

### Progression Events

Events related to player progression and rewards.

| Event ID | Description | Trigger Condition |
|----------|-------------|-------------------|
| `loot_found` | Loot is discovered | Character's loot count increased from old to new state |
| `character_gained_experience` | A character gains XP | Character's experience increased from old to new state |
| `character_healed_event` | A character is healed | Character's current health increased from old to new state |

## Effect Types

Currently, LumeHaven supports one effect type with more planned for future versions.

### Pulse Effect

Creates a quick flash/color pulse on all lamps.

| Field | Type | Description |
|-------|------|-------------|
| `event` | string | The event ID to listen for |
| `effect` | string | Must be `"pulse"` |
| `rgb` | list | `[red, green, blue]` - RGB color values (0-255) |

**Example:**
```yaml
effects:
  - event: "fire_element_active"
    effect: "pulse"
    rgb: [255, 0, 0]
```

**Behavior:**
When the `fire_element_active` event triggers, all configured lamps will pulse red once.

## Adding Custom Events (Advanced)

LumeHaven's event system is extensible. To add custom events:

### Step 1: Create a Custom Condition

```python
# In a custom module, e.g., src/lumehaven/core/custom_conditions.py
from lumehaven.ghs.model import GameState
from lumehaven.core.event_conditions import Condition

class CustomCondition(Condition):
    """Example: Trigger when a specific scenario starts"""
    
    def __init__(self, target_scenario: int):
        self.target_scenario = target_scenario
    
    def matches(self, old_game_state: GameState, new_game_state: GameState) -> bool:
        return (
            old_game_state.scenario != self.target_scenario and
            new_game_state.scenario == self.target_scenario
        )
```

### Step 2: Register the Condition

Add your condition to the `CONDITIONS_MAP` in `src/lumehaven/core/event_conditions.py`:

```python
from lumehaven.core.custom_conditions import CustomCondition

CONDITIONS_MAP = {
    # ... existing conditions ...
    "scenario_1_started": CustomCondition(target_scenario=1),
    "scenario_5_started": CustomCondition(target_scenario=5),
}
```

### Step 3: Use in Configuration

```yaml
effects:
  - event: "scenario_5_started"
    effect: "pulse"
    rgb: [255, 215, 0]  # Gold for scenario 5
```

## See Also

- [Setup Guide](setup-guide.md) - Get LumeHaven running
- [Configuration](configuration.md) - Configure effects in detail
- [Integrations](integrations.md) - Understand how lamps receive effects
- [API Reference](api-reference.md) - Test effects via API
- [Scenes](scenes.md) - Learn about scene-based lighting

# Events & Effects

LumeHaven reacts to in-game events by triggering lighting effects. This document explains the available events, how to configure effects, and how the event system works.

## Event System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        GHS Database                                │
│  Stores game state (characters, monsters, elements, scenario, etc.)│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GameStateFetcher                               │
│  - Polls the SQLite database at configured intervals              │
│  - Retrieves current game state                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DbReadingEventPublisher                          │
│  - Compares old state with new state                              │
│  - Checks conditions against game events                          │
│  - Queues matching events                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Event Queue                                  │
│  - PulseEvent, SceneEvent, etc.                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────┐         ┌─────────────────────┐
│    LampService       │         │   Other Subscribers   │
│  - Receives events   │         │  (future extensibility)│
│  - Applies effects   │         └─────────────────────┘
│  - Updates lamps     │
└─────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Physical Lamps                               │
│  - Color changes, pulses, cycles                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Available Events

LumeHaven tracks state changes and triggers events based on differences between polling intervals. All events are triggered when the game state changes from one value to another.

### Element Events

These events trigger when elements on the Gloomhaven element board change state.

| Event ID | Description | Trigger Condition |
|----------|-------------|-------------------|
| `fire_element_active` | Fire element becomes active | Element was inactive, now active (state: 0 → 1 or 0 → 2) |
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

## Configuring Effects

Effects are configured in the `effects` section of `config.yml`:

```yaml
effects:
  # Element effects
  - event: "fire_element_active"
    effect: "pulse"
    rgb: [255, 0, 0]        # Red
  - event: "ice_element_active"
    effect: "pulse"
    rgb: [0, 255, 255]      # Cyan
  - event: "air_element_active"
    effect: "pulse"
    rgb: [160, 160, 160]    # Gray
  - event: "earth_element_active"
    effect: "pulse"
    rgb: [204, 102, 0]      # Orange
  - event: "light_element_active"
    effect: "pulse"
    rgb: [255, 255, 0]      # Yellow
  - event: "dark_element_active"
    effect: "pulse"
    rgb: [0, 0, 102]        # Dark Blue
  
  # Combat effects
  - event: "monster_spawned"
    effect: "pulse"
    rgb: [255, 0, 0]        # Red (danger)
  - event: "monster_died"
    effect: "pulse"
    rgb: [255, 128, 0]      # Orange (victory)
  - event: "monster_received_damage"
    effect: "pulse"
    rgb: [255, 51, 51]      # Light Red
  - event: "character_died"
    effect: "pulse"
    rgb: [255, 0, 0]        # Red (defeat)
  - event: "Character_received_damage"
    effect: "pulse"
    rgb: [255, 51, 51]      # Light Red
  
  # Progression effects
  - event: "character_healed_event"
    effect: "pulse"
    rgb: [0, 255, 0]        # Green (healing)
  - event: "character_gained_experience"
    effect: "pulse"
    rgb: [0, 0, 255]        # Blue (XP gain)
  - event: "loot_found"
    effect: "pulse"
    rgb: [255, 215, 0]      # Gold (treasure)
```

## Default Effects

The example configuration (`config.yaml.example`) includes a complete set of default effects that work well for most players:

```yaml
effects:
  - event: "fire_element_active"
    effect: "pulse"
    rgb: [255, 0, 0]
  - event: "ice_element_active"
    effect: "pulse"
    rgb: [0, 255, 255]
  - event: "air_element_active"
    effect: "pulse"
    rgb: [160, 160, 160]
  - event: "earth_element_active"
    effect: "pulse"
    rgb: [204, 102, 0]
  - event: "light_element_active"
    effect: "pulse"
    rgb: [255, 255, 0]
  - event: "dark_element_active"
    effect: "pulse"
    rgb: [0, 0, 102]
  - event: "loot_found"
    effect: "pulse"
    rgb: [255, 215, 0]
  - event: "monster_died"
    effect: "pulse"
    rgb: [255, 128, 0]
  - event: "monster_spawned"
    effect: "pulse"
    rgb: [255, 0, 0]
  - event: "monster_received_damage"
    effect: "pulse"
    rgb: [255, 51, 51]
  - event: "character_died"
    effect: "pulse"
    rgb: [255, 0, 0]
  - event: "character_healed_event"
    effect: "pulse"
    rgb: [0, 255, 0]
  - event: "character_gained_experience"
    effect: "pulse"
    rgb: [0, 0, 255]
  - event: "Character_received_damage"
    effect: "pulse"
    rgb: [255, 51, 51]
```

## Recommended Color Schemes

### By Element

| Element | Color | RGB | Hex |
|---------|-------|-----|-----|
| Fire | Red | [255, 0, 0] | #FF0000 |
| Ice | Cyan/Light Blue | [0, 255, 255] | #00FFFF |
| Air | White/Gray | [160, 160, 160] | #A0A0A0 |
| Earth | Brown | [204, 102, 0] | #CC6600 |
| Light | Yellow | [255, 255, 0] | #FFFF00 |
| Dark | Dark Blue | [0, 0, 102] | #000066 |

### By Event Type

| Category | Event | Suggested Color | RGB |
|----------|-------|----------------|-----|
| **Combat** | Damage (monster/character) | Red | [255, 51, 51] |
| **Combat** | Monster spawn | Red | [255, 0, 0] |
| **Combat** | Monster death | Orange | [255, 128, 0] |
| **Healing** | Character healed | Green | [0, 255, 0] |
| **Progression** | XP gained | Blue | [0, 0, 255] |
| **Progression** | Loot found | Gold | [255, 215, 0] |
| **Progression** | Character death | Red | [255, 0, 0] |

### Thematic Color Palettes

**Classic Fantasy:**
- Fire: [255, 69, 0] (Orange-Red)
- Ice: [0, 191, 255] (Deep Sky Blue)
- Earth: [139, 69, 19] (Saddle Brown)
- Air: [211, 211, 211] (Light Gray)
- Light: [255, 255, 224] (Light Yellow)
- Dark: [25, 25, 112] (Midnight Blue)

**High Contrast:**
- Fire: [255, 0, 0]
- Ice: [0, 255, 255]
- Earth: [165, 42, 42] (Brown)
- Air: [255, 255, 255] (White)
- Light: [255, 255, 0]
- Dark: [0, 0, 0] (Black)

**Pastel:**
- Fire: [255, 102, 102]
- Ice: [173, 216, 230] (Light Blue)
- Earth: [205, 133, 63] (Peru)
- Air: [220, 220, 220] (Gainsboro)
- Light: [255, 255, 153] (Light Yellow)
- Dark: [75, 0, 130] (Indigo)

## Testing Effects

You can test your effect configuration without playing Gloomhaven:

### Method 1: Using the API

1. Start LumeHaven with your configuration
2. Manually trigger a scene change:
   ```bash
   curl -X POST http://localhost:5000/scenes/dungeon
   ```
3. The lamps should update to the scene's colors

### Method 2: Using Event Conditions

The event system is tied to game state changes, so you need to play Gloomhaven to trigger most effects. However, you can:

1. Use the `logging_lamp` type to see effect triggers in the console
2. Set a very short `interval_ms` (e.g., 500) for more responsive testing
3. Make changes in the GHS web UI and watch for light changes

### Method 3: Unit Testing

Create tests for your effect configuration:

```python
from lumehaven.core.config import Config, EventEffect
from lumehaven.core.events import PulseEvent, SceneEvent
from lumehaven.lights.lamps import RGB

# Test that events are created correctly
def test_element_effect():
    effect = EventEffect(
        event="fire_element_active",
        effect="pulse",
        rgb=(255, 0, 0)
    )
    # Verify effect configuration
    assert effect.event == "fire_element_active"
    assert effect.effect == "pulse"
    assert effect.rgb == (255, 0, 0)
```

## Performance Considerations

Each time LumeHaven polls the GHS database (`interval_ms`):

1. **Game State Fetch:** Retrieves the complete game state from SQLite
2. **State Comparison:** Compares old state with new state
3. **Condition Checking:** Checks all configured conditions against the state change
4. **Event Triggering:** Queues all matching events
5. **Event Publishing:** Sends events to all subscribers (including LampService)
6. **Effect Application:** Each lamp processes the effect

**Performance Tips:**

- Use `interval_ms: 1000` for a good balance (1 second)
- Use `interval_ms: 500` for more responsive but CPU-intensive monitoring
- Use `interval_ms: 2000-5000` for fewer but potentially delayed effects
- Limit the number of lamps for better performance
- Use `start_on_boot: false` and start manually via API when ready

## Disabling Effects

To disable an effect, simply remove it from the `effects` list in your configuration:

```yaml
effects:
  # Keep only the effects you want
  - event: "fire_element_active"
    effect: "pulse"
    rgb: [255, 0, 0]
  
  # Removed: ice_element_active, air_element_active, etc.
```

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

## Effect Intensity and Duration

Currently, effects have fixed:
- **Pulse duration:** ~300ms per transition (defined in integrations)
- **Pulse count:** 2 transitions (on then off)
- **Cycle duration:** ~3000ms per color (for scene color cycling)

These can be customized by modifying the lamp integration code.

For example, in the Yeelight integration:

```python
def pulse(self, rgb: RGB):
    # Current implementation: 300ms duration, 2 count
    transitions = [RGBTransition(rgb.r, rgb.g, rgb.b, duration=300)]
    flow = Flow(count=2, transitions=transitions)
    self.bulb.start_flow(flow)
```

You could create a custom integration that allows configuration of these values.

## Future Effect Types

The following effect types are planned for future versions:

| Effect Type | Description | Planned Implementation |
|-------------|-------------|-----------------------|
| `fade` | Smooth color transition from current to target | Use Flow with longer duration |
| `strobe` | Rapid flashing | Multiple transitions with short duration |
| `breathe` | Gentle pulsing/breathe effect | Infinite flow with smooth transitions |
| `wave` | Color wave across multiple lamps | Coordinated sequences |
| `random` | Random color changes | Random selection from palette |

## Troubleshooting Effects

### Effects Not Triggering

1. **Check Configuration:**
   ```bash
   # Verify the effect is in your config
   grep -A2 "fire_element_active" config.yml
   ```

2. **Check Lamp Connection:**
   - Verify lamps are powered on
   - Check network connectivity
   - Test with `logging_lamp` type first

3. **Check Game State Changes:**
   - Effects only trigger on state *changes*
   - If an element is already active when LumeHaven starts, it won't trigger until it changes again

4. **Check Logs:**
   ```bash
   # View LumeHaven logs
   docker compose logs lumehaven
   # or
   tail -f app.log
   ```
   Look for:
   - `Event triggered: PulseEvent` messages
   - `Condition triggered: <ConditionName>` messages

5. **Verify Database Path:**
   - Ensure `sqlite_db` path in config points to the correct location
   - Check that the GHS server is writing to the expected location

### Colors Not Matching Expectations

1. **Check RGB Values:**
   - RGB values must be 0-255
   - Verify your values are in the correct range

2. **Lamp Color Space:**
   - Different lamp types may interpret RGB differently
   - Some lamps may have limited color gamut
   - Test with known colors (red, green, blue) first

3. **Brightness Settings:**
   - Some lamps may have their own brightness settings
   - Check if brightness is affecting color appearance

### Effects Triggering Too Often

1. **Check Interval:**
   - If `interval_ms` is too low, effects may trigger multiple times for the same event
   - Try increasing to 1000ms or higher

2. **Check State Stability:**
   - Some game states may fluctuate rapidly
   - Consider adding debouncing logic (future enhancement)

## See Also

- [Quick Start](quick-start.md) - Get LumeHaven running
- [Configuration](configuration.md) - Configure effects in detail
- [Integrations](integrations.md) - Understand how lamps receive effects
- [API Reference](api-reference.md) - Test effects via API
- [Scenes](scenes.md) - Learn about scene-based lighting

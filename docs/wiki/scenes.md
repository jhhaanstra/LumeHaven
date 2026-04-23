# Scenes Guide

Scenes in LumeHaven provide ambient lighting that sets the mood for different locations and situations in Gloomhaven. Unlike effects (which are triggered by game events), scenes are persistent lighting states that you can manually activate or have triggered automatically.

## Scene Concept

A **scene** is a collection of colors that lamps cycle through. When a scene is active:

1. Each lamp is assigned one or more colors from the scene's palette
2. Lamps smoothly transition between their assigned colors
3. The color distribution ensures variety across multiple lamps

```
Scene: "dungeon"
├── Color 1: [0, 0, 100]       (Dark Blue)
├── Color 2: [50, 50, 150]     (Medium Blue)
└── Color 3: [0, 50, 50]       (Teal)

Lamps with scene active:
├── Lamp 1: Cycles through Color 1 → Color 2 → Color 3
├── Lamp 2: Cycles through Color 2 → Color 3 → Color 1
└── Lamp 3: Cycles through Color 3 → Color 1 → Color 2
```

## Built-in Scenes

LumeHaven comes with several pre-configured scenes in `config.yaml.example`:

| Scene Name | Description | Colors | Mood |
|------------|-------------|--------|------|
| `tavern` | Warm, inviting tavern lighting | Orange, Light Orange, Dark Orange | Cozy, Safe |
| `dungeon` | Dark, mysterious dungeon | Dark Blue, Medium Blue, Teal | Dangerous, Unknown |
| `forest` | Natural forest ambiance | Green, Light Green, Dark Green | Natural, Calm |
| `frost` | Cold, icy environment | Light Blue, Cyan, Dark Blue | Cold, Harsh |
| `victory` | Celebratory lighting | Gold, Light Gold, Orange | Triumphant |

### Tavern Scene

```yaml
- name: "tavern"
  colors:
    - [255, 140, 0]    # Dark Orange
    - [255, 200, 100]  # Light Orange
    - [200, 100, 0]    # Brown-Orange
```

**Use Case:** Starting location, city scenes, safe resting areas

### Dungeon Scene

```yaml
- name: "dungeon"
  colors:
    - [0, 0, 100]      # Dark Blue
    - [50, 50, 150]    # Medium Blue
    - [0, 50, 50]      # Teal
```

**Use Case:** Dungeons, ruins, underground locations

### Forest Scene

```yaml
- name: "forest"
  colors:
    - [0, 100, 0]      # Dark Green
    - [50, 200, 50]    # Light Green
    - [0, 50, 0]       # Very Dark Green
```

**Use Case:** Forest scenarios, outdoor locations, nature areas

### Frost Scene

```yaml
- name: "frost"
  colors:
    - [100, 200, 255]  # Light Blue
    - [150, 255, 255]  # Cyan
    - [50, 100, 200]   # Dark Cyan
```

**Use Case:** Winter scenarios, icy locations, cold environments

### Victory Scene

```yaml
- name: "victory"
  colors:
    - [255, 215, 0]    # Gold
    - [255, 255, 100]  # Light Gold
    - [255, 150, 0]    # Orange
```

**Use Case:** Scenario completion, major victories, celebration

## Configuring Scenes

Scenes are configured in the `scenes` section of `config.yml`:

```yaml
scenes:
  - name: "tavern"
    colors:
      - [255, 140, 0]
      - [255, 200, 100]
      - [200, 100, 0]
  - name: "custom_scene"
    colors:
      - [255, 0, 0]
      - [0, 255, 0]
      - [0, 0, 255]
```

### Scene Configuration Options

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique identifier for the scene. Used in API calls and as `main_scene` |
| `colors` | list | Yes | Array of RGB color arrays. Each color is `[red, green, blue]` with values 0-255 |

### Color Selection Tips

**Number of Colors:**
- **1 color:** All lamps will be the same color (static)
- **2-3 colors:** Good balance of variety and simplicity
- **4+ colors:** More variety, but colors may change too frequently

**Color Choice:**
- Use **similar colors** for a cohesive look (e.g., different shades of blue)
- Use **contrasting colors** for visual interest (e.g., red, green, blue)
- Avoid **clashing colors** (e.g., bright red and bright green together)

**Color Temperature:**
- **Warm colors** (reds, oranges, yellows): Cozy, safe, inviting
- **Cool colors** (blues, greens, purples): Dangerous, mysterious, cold
- **Neutral colors** (whites, grays): Neutral, balanced

## Using Scenes

### Setting the Main Scene

The `main_scene` in your configuration is the default scene that activates when LumeHaven starts:

```yaml
main_scene: "tavern"
```

When LumeHaven starts, all lamps will cycle through the colors of the main scene.

### Changing Scenes via API

Use the API to manually change scenes:

```bash
# Activate the dungeon scene
curl -X POST http://localhost:5000/scenes/dungeon

# Activate the forest scene
curl -X POST http://localhost:5000/scenes/forest
```

### Checking Current Scene

```bash
# Get the current active scene
curl http://localhost:5000/scenes/current
# Returns: "dungeon" or "none"

# List all available scenes
curl http://localhost:5000/scenes
# Returns: ["tavern", "dungeon", "forest"]
```

### Automating Scene Changes

You can automate scene changes based on game state:

#### With Home Assistant

```yaml
# automations.yaml
automation:
  - alias: "Set dungeon scene when starting scenario"
    trigger:
      - platform: state
        entity_id: input_select.current_scenario
        to: "Ruins of Gaunt"
    action:
      - service: rest_command.lumehaven_scene
        data:
          scene: "dungeon"

  - alias: "Set tavern scene when returning to town"
    trigger:
      - platform: state
        entity_id: input_select.current_scenario
        to: "Gloomhaven"
    action:
      - service: rest_command.lumehaven_scene
        data:
          scene: "tavern"
```

#### With Node-RED

Create a flow that monitors game state and triggers scene changes accordingly.

#### With Custom Scripts

```python
import requests
import time

BASE_URL = "http://localhost:5000"

# Cycle through scenes every hour
def cycle_scenes():
    scenes = ["tavern", "dungeon", "forest", "frost"]
    while True:
        for scene in scenes:
            requests.post(f"{BASE_URL}/scenes/{scene}")
            time.sleep(3600)  # 1 hour

# Start in a separate thread or process
```

## Scene Behavior

### Color Distribution

When a scene is activated with multiple lamps and multiple colors:

1. LumeHaven uses `itertools.permutations` to create color sequences
2. Sequences are shuffled randomly
3. Each lamp gets a unique sequence from the permutations
4. Lamps cycle through their assigned sequence

**Example:**
```python
# Scene with 2 colors and 2 lamps
colors = [RGB(255, 0, 0), RGB(0, 255, 0)]  # Red, Green

# Permutations: [(Red, Green), (Green, Red)]
# After shuffling: [(Green, Red), (Red, Green)]

# Lamp 1: Green → Red → Green → Red...
# Lamp 2: Red → Green → Red → Green...
```

### Color Transitions

- The transition duration depends on the lamp integration
- Yeelight uses ~3000ms (3 seconds) per transition by default
- Transitions are smooth (not abrupt changes)
- The cycle is infinite (lamp keeps cycling through colors)

## Creating Custom Scenes

### Step-by-Step: Adding a Custom Scene

1. **Decide on a scene name and theme**
   - Example: "cave" for cave scenarios

2. **Choose colors that match the theme**
   - Cave: dark colors with some warm accents (torch light)

3. **Add to config.yml:**
   ```yaml
   scenes:
     - name: "tavern"
       colors:
         - [255, 140, 0]
         - [255, 200, 100]
         - [200, 100, 0]
     - name: "cave"
       colors:
         - [40, 40, 40]      # Dark Gray (cave walls)
         - [100, 50, 0]      # Dark Orange (torch light)
         - [200, 100, 0]     # Orange (bright torch)
   ```

4. **Test the scene:**
   ```bash
   curl -X POST http://localhost:5000/scenes/cave
   ```

5. **Adjust colors as needed**

### Example Custom Scenes

**Sunset Scene:**
```yaml
- name: "sunset"
  colors:
    - [255, 102, 0]    # Orange-Red
    - [255, 153, 51]   # Light Orange
    - [204, 51, 0]     # Dark Orange
```

**Storm Scene:**
```yaml
- name: "storm"
  colors:
    - [0, 0, 51]       # Very Dark Blue
    - [0, 51, 102]     # Dark Blue
    - [102, 102, 153]  # Light Blue with gray tint
    - [255, 255, 255]  # White (lightning flash)
```

**Cursed Scene:**
```yaml
- name: "cursed"
  colors:
    - [100, 0, 100]    # Purple
    - [50, 0, 50]      # Dark Purple
    - [150, 0, 150]    # Light Purple
```

**Blessed Scene:**
```yaml
- name: "blessed"
  colors:
    - [255, 255, 204]  # Light Yellow
    - [255, 255, 153]  # Gold
    - [255, 204, 102]  # Light Orange
```

## Scene Management Tips

### 1. Start with the Defaults

The built-in scenes work well for most scenarios. Start with them and only add custom scenes when you need something specific.

### 2. Test in Isolation

Before adding many scenes, test each one individually:
```bash
curl -X POST http://localhost:5000/scenes/your_new_scene
```

### 3. Use Meaningful Names

Use names that clearly describe the scene's purpose:
- ✅ Good: `"road_event"`, `"city_ruins"`, `"ancient_tomb"`
- ❌ Bad: `"scene1"`, `"colors2"`, `"test3"`

### 4. Keep It Simple

Start with 3 colors per scene. You can add more later if needed, but more colors = more frequent changes.

### 5. Consider Lamp Count

- With **1 lamp:** All colors in the scene will play on that one lamp
- With **2 lamps:** Each lamp gets half the colors (rounded up)
- With **3+ lamps:** Colors are distributed across lamps

## Advanced Scene Usage

### Dynamic Scene Changes

You can trigger scene changes based on in-game events. While LumeHaven doesn't currently have built-in scene triggers for game events, you can:

1. Use the API from a custom script that monitors GHS
2. Use Home Assistant to trigger scene changes based on game state
3. Manually change scenes when a scenario starts

### Scene-Based Automation

Create external scripts that change scenes based on time, scenario, or other factors:

```python
import requests
import sqlite3
import time

BASE_URL = "http://localhost:5000"
DB_PATH = "ghs/ghs.sqlite"

def get_current_scenario():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT scenario FROM games WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def scenario_to_scene(scenario_id):
    # Map scenario IDs to scene names
    mapping = {
        1: "black_barrow",
        2: "barrow",
        3: "ruins",
        # ... add your mappings
    }
    return mapping.get(scenario_id, "tavern")

def monitor_scenario():
    last_scenario = None
    while True:
        current_scenario = get_current_scenario()
        if current_scenario != last_scenario:
            scene = scenario_to_scene(current_scenario)
            requests.post(f"{BASE_URL}/scenes/{scene}")
            last_scenario = current_scenario
        time.sleep(60)  # Check every minute

monitor_scenario()
```

### Scene Blending

Future enhancements could include:
- Gradual transitions between scenes
- Scene layering (multiple scenes active at once)
- Scene intensity controls (brightness, saturation)

## Troubleshooting Scenes

### Scene Not Found

```bash
curl -X POST http://localhost:5000/scenes/nonexistent
# Returns: No scene named: nonexistent
```

**Solution:** Check that the scene name is spelled correctly in both the API call and `config.yml`.

### Scene Not Changing

1. **Verify scene name:**
   ```bash
   curl http://localhost:5000/scenes
   ```

2. **Check current scene:**
   ```bash
   curl http://localhost:5000/scenes/current
   ```

3. **Verify lamps are connected:**
   ```bash
   curl http://localhost:5000/lamps
   ```

4. **Check logs:**
   ```bash
   docker compose logs lumehaven
   ```

### Colors Not Look Good

1. **Adjust color values:** Try different RGB combinations
2. **Change number of colors:** Try with 2-3 colors instead of many
3. **Test with logging_lamp:** Verify the scene is being set correctly

### Scene Changes Too Fast/Slow

The scene transition speed is controlled by the lamp integration, not the scene definition. For Yeelight:
- Transition duration is ~3000ms (3 seconds) per color
- To change this, modify the `duration` parameter in the Yeelight integration code

## Scene Configuration Reference

### Complete Scene Example

```yaml
scenes:
  # Standard scenes
  - name: "tavern"
    colors:
      - [255, 140, 0]
      - [255, 200, 100]
      - [200, 100, 0]
  
  - name: "dungeon"
    colors:
      - [0, 0, 100]
      - [50, 50, 150]
      - [0, 50, 50]
  
  # Custom scenes
  - name: "sunset"
    colors:
      - [255, 102, 0]
      - [255, 153, 51]
      - [204, 51, 0]
  
  - name: "storm"
    colors:
      - [0, 0, 51]
      - [0, 51, 102]
      - [102, 102, 153]
      - [255, 255, 255]
```

### Validation Rules

- `name` must be a unique string
- `colors` must be a list with at least one color
- Each color must be a list/tuple of exactly 3 integers
- Each RGB value must be between 0 and 255 (inclusive)

**Invalid Examples:**
```yaml
# Invalid: RGB values out of range
- name: "bad"
  colors:
    - [300, 0, 0]  # R > 255
    - [0, -1, 0]   # G < 0

# Invalid: Wrong number of color components
- name: "bad"
  colors:
    - [255, 0]     # Only 2 values
    - [255, 0, 0, 255]  # 4 values

# Invalid: Non-integer values
- name: "bad"
  colors:
    - [255.0, 0, 0]  # Float instead of int
    - ["255", 0, 0]   # String instead of int
```

## See Also

- [Quick Start](quick-start.md) - Get LumeHaven running
- [Configuration](configuration.md) - Configure scenes in detail
- [API Reference](api-reference.md) - Control scenes via API
- [Integrations](integrations.md) - How lamps display scenes
- [Events & Effects](events-and-effects.md) - Event-based lighting

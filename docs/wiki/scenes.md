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

## Configuring Scenes

LumeHaven comes with several pre-configured scenes in `config.yaml.example`. Feel free to remove and/or add scenes. Scenes are configured in the `scenes` section of `config.yml`:

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

## See Also

- [Setup Guide](setup-guide.md) - Get LumeHaven running
- [Configuration](configuration.md) - Configure scenes in detail
- [API Reference](api-reference.md) - Control scenes via API
- [Integrations](integrations.md) - How lamps display scenes
- [Events & Effects](events-and-effects.md) - Event-based lighting

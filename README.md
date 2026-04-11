# LumeHaven: Gloomhaven Lighting Integration

LumeHaven connects with [Gloomhaven secretariat](https://github.com/Lurkars/gloomhavensecretariat) and adjusts your light based on the events of the game. You can set scenes that match the party's current place. Light effects will play based on what happens in-game. For example, red flashes on combat damage and green flashes on heals.

---

## Features

- **Server Control:** Start, stop, and check server status.
- **Scene Management:** Predefined lighting scenes for different *Gloomhaven* scenarios.
- **Light effects:** Light effects based on events that happen in-game.

---

## API Endpoints

### Server Management


| Endpoint  | Method | Description                     |
| --------- | ------ | ------------------------------- |
| `/status` | GET    | Check if the server is running. |
| `/start`  | POST   | Start the server.               |
| `/stop`   | POST   | Stop the server.                |


### Scene Management


| Endpoint               | Method | Description                     |
| ---------------------- | ------ | ------------------------------- |
| `/scenes`              | GET    | List all available scenes.      |
| `/scenes/current`      | GET    | Get the currently active scene. |
| `/scenes/<scene_name>` | POST   | Set the active scene by name.   |


### Lamp Management

These endpoints are mainly used for debugging puproses of the lighting integrations.

| Endpoint                        | Method | Description                             |
| ------------------------------- | ------ | --------------------------------------- |
| `/lamps`                        | GET    | List all connected lamps.               |
| `/lamps/<entity_id>`            | GET    | Get configuration for a specific lamp.  |
| `/lamps/<entity_id>/color`      | POST   | Set the color for a specific lamp.      |
| `/lamps/<entity_id>/brightness` | POST   | Set the brightness for a specific lamp. |


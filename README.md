# LumeHaven: Gloomhaven Lighting Integration

LumeHaven connects with [Gloomhaven Secretariat (GHS)](https://github.com/Lurkars/ghs-server) and adjusts your light based on the events of the game. You can set scenes that match the party's current place. Light effects will play based on what happens in-game. For example, red flashes on combat damage and green flashes on heals.

---

## Features

- **Server Control:** Start, stop, and check server status.
- **Scene Management:** Predefined lighting scenes for different *Gloomhaven* scenarios.
- **Light effects:** Light effects based on events that happen in-game.

---

## Setup Guide

This project uses Docker Compose to run both a **Gloomhaven Secretariat (GHS) server** and a **LumeHaven** instance.

### Configuring the GHS Server
To generate a valid LumeHaven configuration, you first need to set up and configure the GHS server:
1. From the project root directory, start the ghs server `docker compose up -d ghs-server`, and open in the browser `localhost:12345`.
   - the ghs directory contains an `application.properties` that automatically downloads the latest client. 

**2. Save Progress to the Server**

By default, GHS saves progress in your browser’s local storage. To save to the server instead:
1. Open the top-left menu and select "Connect to Server".
2. Enter the following details:
   - Host: localhost
   - Port: 12345
   - Game Code: Click "Generate Code" and save the generated UUID (e.g., `74986287-7208-4719-aba3-5fe464f7f713`).
3. Click "Connect". You should now see the server version displayed.

*Tip: Use a private browser window if you encounter connection issues after your first session.*

**3. Set Up Your Campaign**

Proceed to create a new campaign or import your existing data as usual.

**4. Verify the Database**

If you used the provided docker-compose file and started the GHS server from the project root, a `ghs.sqlite` file will be created in the ghs directory.


### Creating a LumeHaven Configuration
Once the GHS server is set up, create a LumeHaven configuration:

**1. Configure config.yaml**

Copy `config.yaml.example` to `config.yaml` and edit it:
- Set game_code to the UUID generated during GHS setup (found in the top-left menu under "Server Connection").
- If LumeHaven is started from the project root, leave the other GHS settings as-is.

**2. Add Your Lamps**

Refer to the wiki (WIP) for detailed instructions on adding lamps.

**3. Customize Effects**

All effects are pre-configured. You can modify color values or remove unwanted effects.

**4. Configure Scenes**

Example scenes are provided. You can override them or add new ones as needed.

### Starting LumeHaven
With the configuration complete, start the LumeHaven server from the project root directory using `docker compose up -d lumehaven`.

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


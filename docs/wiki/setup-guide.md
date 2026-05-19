# Quick Start

## Setup Guide

This project uses Docker Compose to run both a **Gloomhaven Secretariat (GHS) server** and a **LumeHaven** instance.

### Prerequisites

- Docker and Docker Compose installed
- A Gloomhaven Secretariat (GHS) compatible browser

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

## 5. Verify services

- Check server status: `curl http://localhost:5000/status`
- List scenes: `curl http://localhost:5000/scenes`

## 6. Start game loop
In case Lumehaven is not configured to start the game loop on boot (which is disabled by default), you can start the game loop manually with the following command: `curl -X POST http://localhost:5000/start`

## 7. Stopping game loop
You can stop the game loop with the following command: `curl -X POST http://localhost:5000/stop`


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

Now start playing Gloomhaven in your browser, and watch your lights react to in-game events!

## Troubleshooting / FAQ

**Q: Can I use LumeHaven without Docker?**
A: Yes, install dependencies manually and run `python -m lumehaven`.

**Q: Can I use LumeHaven with a GHS server on a different machine?**
A: Not currently. LumeHaven reads the SQLite database directly, so GHS and LumeHaven must share the same filesystem or volume.

**Q: Can I add more lamp types?**
A: Yes! Create a new integration following the [Integrations Guide](integrations.md).

**Q: Can I use LumeHaven with non-Yeelight lamps?**
A: Yes! Use the plugin system to add support for any smart lighting system.

**Q: Can I have different scenes for different scenarios?**
A: Not automatically currently. You can manually change scenes via the API, or create scripts to automate this.

**Q: Why do effects trigger multiple times for the same event?**
A: The polling interval (`interval_ms`) may be catching the game state multiple times during a transition. Try increasing the interval.

**Q: Can I run multiple LumeHaven instances?**
A: Yes, use different config files and port mappings. Each instance controls its own set of lamps.

**Q: How do I reset LumeHaven?**
A: Stop all containers (`docker compose down`), delete `ghs/ghs.sqlite` if needed, and restart GHS to generate a new game code.

**Q: Where are logs stored?**
A: In the container at `/lumehaven/app.log`, or mounted to your host if configured.

**Q: Can I change the API port?**
A: Yes, modify the port mapping in `docker-compose.yml`. LumeHaven itself uses port 5000 internally.

## Version Compatibility

| LumeHaven Version | Python Version | GHS Server | Notes |
|-------------------|----------------|-------------|-------|
| Latest (main) | 3.14+ | Latest | Recommended |
| 0.1.0 | 3.14+ | Any | Stable |

## Next Steps

- [Configuration Reference](configuration.md)
- [Adding Lamp Integrations](integrations.md)

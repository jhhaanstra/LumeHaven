# Troubleshooting Guide

This guide covers common issues and their solutions when using LumeHaven.

## Table of Contents

- [Installation Issues](#installation-issues)
- [GHS Server Problems](#ghs-server-problems)
- [LumeHaven Server Problems](#lumehaven-server-problems)
- [Lamp Connection Issues](#lamp-connection-issues)
- [Configuration Problems](#configuration-problems)
- [Effect and Scene Issues](#effect-and-scene-issues)
- [API Problems](#api-problems)
- [Docker Issues](#docker-issues)
- [Performance Issues](#performance-issues)
- [Logs and Debugging](#logs-and-debugging)
- [Getting Help](#getting-help)

## Installation Issues

### Dependency Installation Fails

**Symptom:** `pip install` or `uv sync` fails with dependency errors.

**Solutions:**

1. **Use uv (recommended):**
   ```bash
   uv sync
   ```

2. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   pip install -e .
   ```

3. **Use a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

4. **Manual dependency installation:**
   ```bash
   pip install flask pydantic pyyaml requests yeelight apscheduler
   ```

5. **Check Python version:**
   ```bash
   python --version
   ```
   LumeHaven requires Python 3.14+. Upgrade if needed.

### Docker Build Fails

**Symptom:** `docker compose build` fails.

**Solutions:**

1. **Ensure Docker is running:**
   ```bash
   docker --version
   docker compose version
   ```

2. **Check Docker memory allocation:**
   - Open Docker Desktop settings
   - Increase memory to at least 4GB

3. **Clean and rebuild:**
   ```bash
   docker compose down --rmi all
   docker compose build --no-cache
   ```

4. **Check Dockerfile:**
   Ensure the Dockerfile specifies the correct Python version.

## GHS Server Problems

### GHS Server Won't Start

**Symptom:** `docker compose up -d ghs-server` fails or container exits immediately.

**Solutions:**

1. **Check container logs:**
   ```bash
   docker compose logs ghs-server
   ```

2. **Verify port availability:**
   ```bash
   lsof -i :12345
   lsof -i :8080
   ```
   If ports are in use, change them in `docker-compose.yml`.

3. **Check volume permissions:**
   ```bash
   mkdir -p ghs
   chmod -R 777 ghs
   ```

4. **Pull latest image:**
   ```bash
   docker compose pull ghs-server
   docker compose up -d ghs-server
   ```

5. **Increase Docker resources:**
   - Docker Desktop: Settings → Resources → Increase memory/CPU

### GHS Web UI Not Accessible

**Symptom:** Cannot access `http://localhost:12345`.

**Solutions:**

1. **Verify container is running:**
   ```bash
   docker compose ps
   ```

2. **Check port mapping:**
   ```bash
   docker port luma-ghs-server-1 8080
   ```

3. **Test from different browser:**
   Try Chrome, Firefox, or Edge.

4. **Check firewall:**
   ```bash
   # On macOS
   sudo pfctl -sr | grep 12345
   
   # On Linux
   sudo ufw status
   ```

5. **Clear browser cache:**
   Sometimes old cached data causes issues.

### Cannot Connect to GHS Server

**Symptom:** GHS web UI loads but says "Not connected to server".

**Solutions:**

1. **Use correct connection details:**
   - Host: `localhost` (or your Docker host IP)
   - Port: `12345` (external port)
   - Game Code: Generate a new one

2. **Use incognito/private window:**
   Local storage issues can prevent connection.

3. **Clear GHS local storage:**
   - In browser dev tools: Application → Local Storage → Clear `ghs-server` data
   - Or use a different browser profile

4. **Verify volume mount:**
   ```bash
   ls -la ghs/
   ```
   Should see `ghs.sqlite` after first connection.

### Game Code Not Working

**Symptom:** Invalid game code or connection refused.

**Solutions:**

1. **Generate new game code:**
   - In GHS UI: Menu → Connect to Server → Generate Code

2. **Verify game_code in config.yml:**
   ```bash
   grep game_code config.yml
   ```
   Ensure it matches the code from GHS UI.

3. **Check database file:**
   ```bash
   sqlite3 ghs/ghs.sqlite "SELECT * FROM game_codes;"
   ```
   Verify your game_code exists.

## LumeHaven Server Problems

### LumeHaven Won't Start

**Symptom:** `python -m lumehaven` exits with error or hangs.

**Solutions:**

1. **Check configuration file:**
   ```bash
   python -c "from lumehaven.core.config import Config; Config.from_file('config.yml')"
   ```
   This validates your config.

2. **Missing config.yml:**
   ```bash
   cp config.yaml.example config.yml
   # Edit config.yml with your settings
   ```

3. **Check for missing dependencies:**
   ```bash
   python -c "import flask; import pydantic; import yaml; import requests"
   ```

4. **View error messages:**
   ```bash
   python -m lumehaven 2>&1 | tee start.log
   ```

### LumeHaven Exits Immediately

**Symptom:** Server starts but exits after a few seconds.

**Solutions:**

1. **Check for configuration errors:**
   ```bash
   docker compose logs lumehaven
   ```
   Look for validation errors.

2. **Verify SQLite database exists:**
   ```bash
   ls -la ghs/ghs.sqlite
   ```
   Start GHS first to create the database.

3. **Check paths in config.yml:**
   Ensure `sqlite_db` path is correct:
   ```yaml
   ghs:
     sqlite_db: "ghs/ghs.sqlite"
   ```

4. **Run in foreground for debugging:**
   ```bash
   docker compose up lumehaven
   ```
   (Without `-d` flag)

### Server Starts but No Lights Change

**Symptom:** LumeHaven is running but lamps don't respond.

**Solutions:**

1. **Check if monitoring is started:**
   ```bash
   curl http://localhost:5000/status
   ```
   If `{"started": false}`, start it:
   ```bash
   curl -X POST http://localhost:5000/start
   ```

2. **Verify lamp configuration:**
   ```bash
   curl http://localhost:5000/lamps
   ```

3. **Test with logging_lamp:**
   Temporarily use `logging_lamp` type to verify events are triggering:
   ```yaml
   lamps:
     - type: "logging_lamp"
       id: "test"
   ```

4. **Check start_on_boot setting:**
   If `start_on_boot: false`, you must manually start monitoring.

## Lamp Connection Issues

### Lamps Not Connecting

**Symptom:** Lamps don't respond to commands.

**Solutions by Lamp Type:**

#### Yeelight Bulbs

1. **Verify IP address:**
   ```bash
   ping 192.168.0.42
   ```

2. **Check bulb is powered on:**
   physical light should be on.

3. **Enable developer mode:**
   - In Yeelight app: Device → Enable Developer Mode
   - Or cycle power 5 times quickly

4. **Check network connectivity:**
   Ensure bulb and LumeHaven are on same network.

5. **Test with yeelight CLI:**
   ```bash
   python -c "from yeelight import Bulb; b = Bulb('192.168.0.42'); b.set_rgb(255, 0, 0)"
   ```

6. **Firewall/antivirus:**
   Temporarily disable to test.

#### Philips Hue / Other Integrations

1. **Verify IP address of bridge**
2. **Check bridge connectivity**
3. **Verify API keys / authentication**
4. **Test with official SDK first**

### All Lamp Types

1. **Check network firewall:**
   ```bash
   # On Linux/macOS
   ping <lamp-ip>
   telnet <lamp-ip> <lamp-port>
   ```

2. **Verify lamp is on LAN mode:**
   Most smart bulbs support both LAN and cloud modes. LAN mode is required.

3. **Restart lamp:**
   Power cycle the physical lamp.

4. **Check for IP changes:**
   Your router may have assigned a new IP. Use DHCP reservation.

5. **Verify subnet:**
   All devices must be on the same subnet.

## Configuration Problems

### Invalid Configuration

**Symptom:** LumeHaven fails to start with validation error.

**Solutions:**

1. **Validate YAML syntax:**
   ```bash
   python -c "import yaml; yaml.safe_load(open('config.yml'))"
   ```

2. **Check for tabs:**
   YAML is space-sensitive. Use spaces, not tabs.

3. **Verify required fields:**
   ```yaml
   ghs:
     game_code: ""  # Required
     sqlite_db: ""  # Required
     url: ""       # Required
     interval_ms: 1000  # Required
   main_scene: ""  # Required
   lamps: []      # Required
   ```

4. **Check RGB values:**
   RGB values must be 0-255:
   ```yaml
   effects:
     - event: "test"
       effect: "pulse"
       rgb: [255, 0, 0]  # Valid
       # rgb: [300, 0, 0]  # Invalid - R > 255
       # rgb: [-1, 0, 0]   # Invalid - G < 0
   ```

5. **Check scene references:**
   `main_scene` must match a scene name:
   ```yaml
   main_scene: "tavern"  # Must exist in scenes list
   scenes:
     - name: "tavern"  # OK
     # - name: "dungeon"  # If main_scene was "dungeon", it would error
   ```

### Configuration File Not Found

**Symptom:** "File not found" or "No such file" error.

**Solutions:**

1. **Verify filename:**
   ```bash
   ls -la config.*
   ```
   Should be `config.yml`, not `config.yaml` (though YAML files work with either extension).

2. **Check file location:**
   LumeHaven looks for `config.yml` in the current directory.
   ```bash
   pwd
   ls -la config.yml
   ```

3. **Use absolute path:**
   ```bash
   python -m lumehaven --config /path/to/config.yml
   ```
   Or in Docker, ensure the volume is mounted:
   ```yaml
   volumes:
     - ./config.yml:/lumehaven/config.yml
   ```

4. **Verify Docker volume:**
   ```bash
   docker exec luma-lumehaven-1 ls -la /lumehaven/config.yml
   ```

### GHS Database Path Incorrect

**Symptom:** "Database not found" or "Unable to connect to SQLite".

**Solutions:**

1. **Verify database exists:**
   ```bash
   ls -la ghs/ghs.sqlite
   ```

2. **Check path in config.yml:**
   ```yaml
   ghs:
     sqlite_db: "ghs/ghs.sqlite"  # Relative to LumeHaven working dir
   ```

3. **Use absolute path:**
   ```yaml
   ghs:
     sqlite_db: "/full/path/to/ghs/ghs.sqlite"
   ```

4. **Docker volume mapping:**
   Ensure both containers share the same volume:
   ```yaml
   services:
     ghs-server:
       volumes:
         - ./ghs:/root/.ghs
     lumehaven:
       volumes:
         - ./ghs:/lumehaven/ghs
   ```

## Effect and Scene Issues

### Effects Not Triggering

**Symptom:** Game events occur but no lighting effects.

**Solutions:**

1. **Start game monitoring:**
   ```bash
   curl -X POST http://localhost:5000/start
   curl http://localhost:5000/status  # Verify started: true
   ```

2. **Verify event configuration:**
   ```bash
   grep -A2 "fire_element_active" config.yml
   ```

3. **Check logs for triggers:**
   ```bash
   docker compose logs lumehaven | grep "Event triggered"
   ```
   Look for:
   - `INFO - Event triggered: PulseEvent`
   - `INFO - Condition triggered: FireElementActive`

4. **Test with logging_lamp:**
   Use `logging_lamp` to verify effects are being sent:
   ```yaml
   lamps:
     - type: "logging_lamp"
       id: "debug"
   ````

5. **Check GHS database updates:**
   Ensure the GHS server is saving to the database:
   ```bash
   sqlite3 ghs/ghs.sqlite "SELECT * FROM games;"
   ```

6. **Verify game_code:**
   Ensure `game_code` in config matches GHS server.

7. **Check interval_ms:**
   Actions may take up to `interval_ms` milliseconds to trigger:
   ```yaml
   ghs:
     interval_ms: 1000  # Wait up to 1 second
   ```
   For testing, temporarily reduce to 500.

### Scenes Not Changing

**Symptom:** Manually setting scenes via API doesn't work.

**Solutions:**

1. **Verify scene exists:**
   ```bash
   curl http://localhost:5000/scenes
   ```

2. **Check scene name spelling:**
   ```bash
   curl -X POST http://localhost:5000/scenes/dungeon
   # Not: dungeon, Dungeon, DUNGEON
   ```

3. **Verify lamps are configured:**
   ```bash
   curl http://localhost:5000/lamps
   ```
   If empty, add lamps to config.yml.

4. **Test with API:**
   ```bash
   curl -X POST http://localhost:5000/scenes/dungeon
   curl http://localhost:5000/scenes/current
   ```

5. **Check lamp integration:**
   Test direct lamp control:
   ```bash
   curl -X POST http://localhost:5000/lamps/living-room-lamp/color \
     -H "Content-Type: application/json" \
     -d '{"r": 255, "g": 0, "b": 0}'
   ```

### Colors Don't Look Right

**Symptom:** Colors appear different than expected.

**Solutions:**

1. **Verify RGB values in config:**
   ```yaml
   effects:
     - event: "test"
       effect: "pulse"
       rgb: [255, 0, 0]  # Pure red
   ```

2. **Check lamp color gamut:**
   Different lamp models have different color capabilities. Some may not display pure RGB well.

3. **Try different colors:**
   ```yaml
   scenes:
     - name: "test"
       colors:
         - [255, 0, 0]    # Pure red
         - [0, 255, 0]    # Pure green  
         - [0, 0, 255]    # Pure blue
   ```

4. **Adjust brightness:**
   Some lamps blend colors better at lower brightness.

5. **Use HSV/HSL converter:**
   Convert colors using online tools to ensure correct RGB values.

## API Problems

### API Not Responding

**Symptom:** `curl` commands hang or return connection refused.

**Solutions:**

1. **Verify server is running:**
   ```bash
   docker compose ps
   ```

2. **Check port mapping:**
   ```bash
   docker port luma-lumehaven-1 5000
   ```

3. **Test from same machine:**
   ```bash
   curl http://localhost:5000/status
   ```

4. **Check container IP:**
   ```bash
   docker inspect luma-lumehaven-1 | grep IPAddress
   curl http://<container-ip>:5000/status
   ```

5. **Verify Flask is listening:**
   ```bash
   docker exec luma-lumehaven-1 netstat -tuln | grep 5000
   ```

### API Returns 404

**Symptom:** API endpoints return 404 Not Found.

**Solutions:**

1. **Verify endpoint URL:**
   ```bash
   curl http://localhost:5000/status      # Valid
   curl http://localhost:5000/invalid     # 404
   ```

2. **Check trailing slashes:**
   Flask ignores trailing slashes, but be consistent:
   ```bash
   curl http://localhost:5000/scenes      # OK
   curl http://localhost:5000/scenes/     # Also OK
   ```

3. **Verify scene/lamp names:**
   ```bash
   curl -X POST http://localhost:5000/scenes/WrongName
   # Returns: No scene named: WrongName
   ```

4. **List available resources:**
   ```bash
   curl http://localhost:5000/scenes
   curl http://localhost:5000/lamps
   ```

### API Returns 500 Error

**Symptom:** Internal server error.

**Solutions:**

1. **Check server logs:**
   ```bash
   docker compose logs lumehaven
   ```

2. **Test with minimal config:**
   Simplify config to isolate issue.

3. **Verify database connectivity:**
   ```bash
   docker exec luma-lumehaven-1 python -c \
     "import sqlite3; conn = sqlite3.connect('ghs/ghs.sqlite'); print('OK')"
   ```

4. **Check file permissions:**
   ```bash
   docker exec luma-lumehaven-1 ls -la /lumehaven/ghs/
   ```

## Docker Issues

### Docker Compose Hangs

**Symptom:** `docker compose up` hangs or takes forever.

**Solutions:**

1. **Check container logs:**
   ```bash
   docker compose logs -f
   ```
   (In another terminal)

2. **Increase timeout:**
   ```bash
   export COMPOSE_HTTP_TIMEOUT=120
   docker compose up
   ```

3. **Pull images first:**
   ```bash
   docker compose pull
   docker compose up -d
   ```

4. **Check disk space:**
   ```bash
   df -h
   ```
   Docker needs sufficient disk space for images.

### Container Restarts Continuously

**Symptom:** Container starts and restarts in a loop.

**Solutions:**

1. **Check exit code:**
   ```bash
   docker inspect luma-lumehaven-1 --format='{{.State.ExitCode}}'
   ```

2. **View logs for last run:**
   ```bash
   docker compose logs --tail=50 lumehaven
   ```

3. **Common causes:**
   - Missing config.yml
   - Invalid configuration
   - Missing SQLite database
   - Permission errors

4. **Run interactively:**
   ```bash
   docker compose run --rm lumehaven sh
   python -m lumehaven
   ```

### Volumes Not Mounting

**Symptom:** Changes to config.yml aren't reflected in container.

**Solutions:**

1. **Verify file exists on host:**
   ```bash
   ls -la config.yml
   ```

2. **Check container mount:**
   ```bash
   docker inspect luma-lumehaven-1 | grep config.yml
   ```

3. **Verify file in container:**
   ```bash
   docker exec luma-lumehaven-1 ls -la /lumehaven/config.yml
   ```

4. **Restart with volume recreating:**
   ```bash
   docker compose down
   docker compose up -d
   ```

5. **Check file permissions:**
   ```bash
   chmod 644 config.yml
   ```

## Performance Issues

### High CPU Usage

**Symptom:** LumeHaven using too much CPU.

**Solutions:**

1. **Increase interval_ms:**
   ```yaml
   ghs:
     interval_ms: 2000  # Check every 2 seconds instead of 1
   ```

2. **Reduce number of lamps:**
   Each lamp adds processing overhead.

3. **Use simpler effects:**
   Complex transitions use more CPU.

4. **Check for tight loops:**
   Could be a bug in an integration.

5. **Profile:**
   ```bash
   # Requires py-spy
   py-spy top --pid $(pgrep -f lumehaven)
   ```

### Slow Response

**Symptom:** API requests or lamp updates are slow.

**Solutions:**

1. **Check lamp response time:**
   Some lamps (especially WiFi bulbs) have latency.

2. **Verify network:**
   Test connectivity to lamp IPs.

3. **Reduce polling:**
   Higher `interval_ms` means less frequent updates.

4. **Use local network:**
   Avoid WiFi if possible for lamp connections.

5. **Check SQLite performance:**
   ```bash
   docker exec luma-lumehaven-1 python -c \
     "import sqlite3; import time; start=time.time(); \
      conn=sqlite3.connect('ghs/ghs.sqlite'); \
      conn.execute('SELECT * FROM games'); conn.close(); \
      print(time.time()-start)"
   ```

### Lamp Update Lag

**Symptom:** Color changes take seconds to appear.

**Solutions:**

1. **Yeelight specific:**
   The yeelight library may have delays. Try:
   ```python
   # In YeeLightLamp.cycle():
   # Change duration from 3000 to 1000
   ```

2. **Network latency:**
   Test with `ping` to lamp IP.

3. **Lamp firmware:**
   Update lamp firmware via manufacturer's app.

4. **Use logging_lamp:**
   Verify the delay is not in light transmission but in LumeHaven itself.

## Logs and Debugging

### Viewing Logs

**Docker:**
```bash
# View all logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View specific service logs
docker compose logs lumehaven

# View last N lines
docker compose logs --tail=50 lumehaven
```

**Direct Python:**
```bash
# Run with verbose output
python -m lumehaven

# Log file
cat app.log

# Tail log file
tail -f app.log
```

### Enabling Debug Logging

Edit `src/lumehaven/__init__.py` to add more verbose logging:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    ...
)
```

Or set via environment variable:
```bash
docker compose run -e PYTHON_LOG_LEVEL=DEBUG lumehaven
```

### Key Log Messages

| Message | Meaning | Action |
|---------|---------|--------|
| `Found integration type: yeelight` | Plugin loaded successfully | ✅ Normal |
| `Loading config` | Configuration being loaded | ✅ Normal |
| `Started on boot` | Game monitoring auto-started | ✅ Normal |
| `GameState(...)` | Game state fetched | ✅ Normal |
| `Event triggered: PulseEvent` | Light effect triggered | ✅ Normal |
| `Condition triggered: FireElementActive` | Game event detected | ✅ Normal |
| `No such file or directory` | File not found | ❌ Fix path |
| `ValidationError` | Invalid config | ❌ Fix config |
| `Connection refused` | Cannot connect to SQLite | ❌ Check DB path |
| `Unknown lamp type` | Invalid lamp type | ❌ Check lamp config |

### Debugging Event Flow

1. **Enable debug logging** (as above)
2. **Use logging_lamp**
3. **Check each step:**
   ```bash
   # 1. Is game state changing?
   docker compose exec luma-lumehaven-1 sqlite3 ghs/ghs.sqlite "SELECT * FROM games;"
   
   # 2. Is LumeHaven detecting changes?
   docker compose logs lumehaven | grep "GameState"
   
   # 3. Are conditions triggering?
   docker compose logs lumehaven | grep "Condition triggered"
   
   # 4. Are events being published?
   docker compose logs lumehaven | grep "Event triggered"
   
   # 5. Are lamps receiving events?
   docker compose logs lumehaven | grep "Pulsing\|Turning color"
   ```

### Debugging Lamp Issues

1. **Test with logging_lamp:**
   ```yaml
   lamps:
     - type: "logging_lamp"
       id: "debug"
   ```
   Check console for "Turning color" messages.

2. **Test direct control:**
   ```bash
   curl -X POST http://localhost:5000/lamps/debug/color \
     -H "Content-Type: application/json" \
     -d '{"r": 255, "g": 0, "b": 0}'
   ```
   Should see "Turning color RGB(r=255, g=0, b=0)" in logs.

3. **Test with yeelight CLI:**
   ```bash
   python -c "from yeelight import Bulb; b = Bulb('192.168.0.42'); b.set_rgb(255, 0, 0)"
   ```

4. **Check network connectivity:**
   ```bash
   ping 192.168.0.42
   nc -zv 192.168.0.42 55443  # Yeelight default port
   ```

## Getting Help

### Before Asking for Help

1. **Check this guide** for your issue
2. **Search existing issues** in the repository
3. **Gather information:**
   - LumeHaven version (from git or pyproject.toml)
   - Docker version (`docker --version`)
   - Python version (`python --version`)
   - OS and version
   - Relevant config.yml sections (redact sensitive info)
   - Log output showing the error

### How to Report Issues

When reporting an issue, include:

1. **Steps to reproduce:**
   - What did you do?
   - What did you expect?
   - What happened instead?

2. **Configuration:**
   ```yaml
   # Relevant parts of config.yml
   ghs:
     game_code: "XXX"
     interval_ms: 1000
   main_scene: "tavern"
   lamps:
     - type: "yeelight"
       id: "my-lamp"
       ip: "192.168.0.42"
   ```

3. **Environment:**
   ```
   - OS: macOS 14.3
   - Docker: 24.0.7
   - Python: 3.14.0
   - LumeHaven: main branch, commit abc123
   ```

4. **Logs:**
   ```
   # Last 50 lines of logs
   [2024-04-23 12:00:00] INFO - Loading config
   [2024-04-23 12:00:01] INFO - Found integration type: yeelight
   ...
   ```

### Common Solutions Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| GHS won't start | `docker compose pull ghs-server; docker compose up -d` |
| LumeHaven won't start | `cp config.yaml.example config.yml && edit config.yml` |
| Config validation error | Check YAML syntax, RGB values (0-255), scene names |
| Lamps not connecting | Verify IP, test with `ping`, use `logging_lamp` first |
| Effects not triggering | `curl -X POST http://localhost:5000/start` |
| API not responding | `docker compose logs lumehaven` |
| Colors wrong | Check RGB values, test with logging_lamp |
| Database not found | Start GHS first, check SQLite path in config |

## FAQ

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

## See Also

- [README](README.md) - Project overview
- [Quick Start](quick-start.md) - Get running quickly
- [Setup Guide](setup-guide.md) - Detailed setup
- [Configuration](configuration.md) - All config options
- [Integrations](integrations.md) - Lamp plugin system
- [API Reference](api-reference.md) - REST API documentation
- [Events & Effects](events-and-effects.md) - Game event system
- [Scenes](scenes.md) - Scene-based lighting

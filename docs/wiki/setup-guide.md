# Setup Guide

Complete instructions for setting up LumeHaven with Gloomhaven Secretariat (GHS).

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Browser                               │
│  ┌─────────────────┐    ┌─────────────────┐                      │
│  │  Gloomhaven      │───▶│  GHS Web UI      │                      │
│  │  (in browser)    │    │  (localhost:12345)│                      │
│  └─────────────────┘    └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GHS Server Docker Container                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  GHS Server (gloomhavensecretariat/ghs-server:latest)      │    │
│  │  - Stores game state in ghs/ghs.sqlite                      │    │
│  │  - Serves web UI on port 8080 (mapped tolocalhost:12345) │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LumeHaven Server Docker Container               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  LumeHaven Server                                            │    │
│  │  - Reads game state from ghs/ghs.sqlite                     │    │
│  │  - Triggers lighting effects based on game events           │    │
│  │  - API on port 5000 (mapped to localhost:5000)              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Your smart lamps                            │
│  (Yeelight, Philips Hue, etc. - configured via plugins)          │
└─────────────────────────────────────────────────────────────────┘
```

## Method 1: Docker Compose (Recommended)

The easiest way to run LumeHaven is using Docker Compose, which handles both the GHS Server and LumeHaven services.

### Step 1: Create docker-compose.yml

The repository includes a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  ghs-server:
    image: gloomhavensecretariat/ghs-server
    ports:
      - "12345:8080"
    volumes:
      - ./ghs:/root/.ghs
  lumehaven:
    image: jhhaanstra/lumehaven
    ports:
      - "5000:5000"
    volumes:
      - ./config.yml:/lumehaven/config.yml
      - ./ghs:/lumehaven/ghs
```

### Step 2: Start the Services

```bash
# From the project root directory
docker compose up -d
```

This will:
1. Pull the GHS Server image
2. Pull the LumeHaven image
3. Create a `ghs/` directory for GHS data
4. Start both services in detached mode

### Step 3: Verify Services

```bash
# Check running containers
docker compose ps

# View logs for GHS Server
docker compose logs ghs-server

# View logs for LumeHaven
docker compose logs lumehaven
```

## Method 2: Running Without Docker

For development or advanced use cases, you can run LumeHaven directly.

### Prerequisites

- Python 3.14+
- pip/uv for dependency management

### Step 1: Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Step 2: Install GHS Server

You'll need to run GHS Server separately:

```bash
# Using Docker (recommended)
docker run -d -p 12345:8080 -v $(pwd)/ghs:/root/.ghs gloomhavensecretariat/ghs-server

# Or install natively (see GHS documentation)
```

### Step 3: Configure GHS

1. Open `http://localhost:12345` in your browser
2. Connect to the server:
   - Host: `localhost`
   - Port: `12345`
   - Generate a game code and save the UUID
3. Create or import your campaign

### Step 4: Configure LumeHaven

Copy and edit the config:

```bash
cp config.yaml.example config.yml
# Edit config.yml with your game_code
```

### Step 5: Run LumeHaven

```bash
# Development mode
python -m lumehaven

# Or use the entry point
lumehaven
```

The server will start on `http://localhost:5000`

## Configuring GHS Server

### Automatic Configuration

The provided `ghs/application.properties` file (if present) can automatically configure GHS to download the latest client data.

### Manual Setup

1. **First Run**: Access `http://localhost:12345` and the client will be downloaded automatically
2. **Server Connection**: 
   - Click the hamburger menu (top-left)
   - Select "Connect to Server"
   - Enter connection details
   - Click "Generate Code" to create a game code
   - Save this UUID for LumeHaven configuration

3. **Verify Database**: After connecting, a `ghs.sqlite` file will be created in the `ghs/` directory

### GHS Directory Structure

```
ghs/
├── application.properties    # GHS configuration
├── ghs.sqlite               # Game database (created automatically)
└── ...                      # Other GHS files
```

## Configuring LumeHaven

See [Configuration Reference](configuration.md) for detailed configuration options.

### Quick Configuration

1. Set `game_code` in `config.yml` to match your GHS game code
2. Add your lamps under the `lamps` section
3. Customize effects and scenes as desired

## Starting/Stopping Services

### Docker Compose Commands

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d ghs-server
docker compose up -d lumehaven

# Stop all services
docker compose down

# Stop specific service
docker compose stop lumehaven

# View logs
docker compose logs -f

# Rebuild images (if you made code changes)
docker compose build
```

### API Commands

Once running, you can control LumeHaven via its API:

```bash
# Check status
curl http://localhost:5000/status

# Start game monitoring
curl -X POST http://localhost:5000/start

# Stop game monitoring
curl -X POST http://localhost:5000/stop
```

## Network Configuration

### Ports

| Service | Internal Port | External Port | Purpose |
|---------|---------------|---------------|---------|
| GHS Server | 8080 | 12345 | Web UI and API |
| LumeHaven | 5000 | 5000 | REST API |

### Changing Ports

To change ports, edit `docker-compose.yml`:

```yaml
services:
  ghs-server:
    ports:
      - "NEW_PORT:8080"  # Change to your desired port
  lumehaven:
    ports:
      - "NEW_PORT:5000"  # Change to your desired port
```

Then update your configuration accordingly.

## Data Persistence

Both services persist data to your host machine:

- **GHS Data**: Stored in `./ghs/` (mounted from container)
- **LumeHaven Config**: Stored in `./config.yml` (mounted from container)

This ensures your data persists even when containers are stopped or restarted.

## Security Considerations

1. **Local Network Only**: By default, services are accessible only from your local machine
2. **No Authentication**: The LumeHaven API does not currently support authentication
3. **Game Code**: Your game code acts as a simple access control mechanism

For production use, consider:
- Adding a reverse proxy with authentication
- Restricting access to trusted IP addresses
- Using Docker's network isolation features

## Next Steps

- [Configuration Reference](configuration.md) - Customize your setup
- [integrations](integrations.md) - Add support for your smart lights
- [API Reference](api-reference.md) - Automate and integrate with other tools

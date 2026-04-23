# Quick Start

Get LumeHaven up and running in minutes with this quick start guide.

## Prerequisites

- Docker and Docker Compose installed
- A Gloomhaven Secretariat (GHS) compatible browser

## Step 1: Clone and Start

```bash
# Clone the repository (if not already done)
git clone https://github.com/your-repo/lumehaven.git
cd lumehaven

# Start both GHS Server and LumeHaven
docker compose up -d
```

This starts:
- **GHS Server** on `http://localhost:12345`
- **LumeHaven Server** on `http://localhost:5000`

## Step 2: Configure GHS Server

1. Open `http://localhost:12345` in your browser
2. Click the top-left menu and select "Connect to Server"
3. Enter:
   - Host: `localhost`
   - Port: `12345`
   - Click "Generate Code" and save the UUID
4. Click "Connect"

## Step 3: Configure LumeHaven

1. Copy the example config:
   ```bash
   cp config.yaml.example config.yml
   ```

2. Edit `config.yml` and set the `game_code` to the UUID from Step 2

3. Add your lamps (see [Configuration](configuration.md) for details)

## Step 4: Start LumeHaven

```bash
# If using Docker (recommended)
docker compose up -d lumehaven

# Or run directly
docker compose up -d ghs-server  # Make sure GHS is running
python -m lumehaven
```

## Step 5: Verify

- Check server status: `curl http://localhost:5000/status`
- List scenes: `curl http://localhost:5000/scenes`
- Start the game loop: `curl -X POST http://localhost:5000/start`

Now start playing Gloomhaven in your browser, and watch your lights react to in-game events!

## Next Steps

- [Detailed Setup Guide](setup-guide.md)
- [Configuration Reference](configuration.md)
- [Adding Lamp Integrations](integrations.md)

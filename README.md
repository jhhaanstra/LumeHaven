# LumeHaven - A Gloomhaven Secretariat Lighting Integration

To run the server:
```commandline
uv run flask --app src.core.app run --debug
```


# Setting Up Gloomhaven Secretariat (GHS)

## **Docker Compose Setup**

- The `docker-compose.yml` in the project root sets up a **GHS server** with a mounted volume.
- The volume maps to the `ghs` folder in your project root, where the `ghs.sqlite` file stores all game data.

## **Accessing the Client**

The server also hosts a client interface at:  
`**http://localhost:12345**`

### **Steps to Connect the Client to the Server**

1. **Open the Client**: Navigate to `http://localhost:12345` in your browser.
2. **Open Settings**: Click the settings menu (top-left corner).
3. **Connect to Server**:
  - Enter the server address: `host: localhost`
  - Enter the port: `12345`
4. **Use the Client**: All game state changes are now saved to the `ghs.sqlite` database in the server component.
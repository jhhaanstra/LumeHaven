# LumeHaven Wiki

Welcome to the LumeHaven Wiki! This documentation covers everything you need to know about setting up, configuring, and extending LumeHaven.

## Table of Contents
- **[Setup Guide](setup-guide.md)** - Get LumeHaven running with Docker
- **[Configuration](configuration.md)** - Understanding and customizing config.yml
- **[Integrations](integrations.md)** - How lamp integrations work and how to create your own
- **[API Reference](api-reference.md)** - Complete endpoint documentation for the LumeHaven server
- **[Events & Effects](events-and-effects.md)** - Available game events and lighting effects
- **[Scenes](scenes.md)** - Creating and managing lighting scenes

## Overview

LumeHaven connects with [Gloomhaven Secretariat (GHS)](https://github.com/Lurkars/ghs-server) to create dynamic lighting effects based on in-game events. As you play Gloomhaven, LumeHaven automatically:

- Changes lighting scenes based on your location (tavern, dungeon, forest, etc.)
- Creates visual effects for game events (combat damage, heals, loot, element activation, etc.)
- Supports multiple lamp types through a plugin architecture

The system consists of:
1. **GHS Server** - Stores your Gloomhaven campaign data
2. **LumeHaven Server** - Monitors game state and triggers lighting effects
3. **Lamp Integrations** - Plugins that control the lamps

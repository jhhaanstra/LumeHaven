# LumeHaven Documentation

This directory contains the complete documentation for LumeHaven.

## Wiki Contents

The [wiki/](./wiki/) directory contains comprehensive guides and references:

### Quick Start
- **[Quick Start](wiki/quick-start.md)** - Get LumeHaven running in minutes with Docker

### Setup & Installation
- **[Setup Guide](wiki/setup-guide.md)** - Complete instructions for setting up GHS Server and LumeHaven
- **[Troubleshooting](wiki/troubleshooting.md)** - Common issues and solutions

### Configuration
- **[Configuration Reference](wiki/configuration.md)** - All configuration options explained with examples

### Development & Customization
- **[Integrations Guide](wiki/integrations.md)** - How lamp integrations work and how to create your own

### API Documentation
- **[API Reference](wiki/api-reference.md)** - Complete endpoint documentation for the LumeHaven server

### Game Features
- **[Events & Effects](wiki/events-and-effects.md)** - Available game events and lighting effects
- **[Scenes Guide](wiki/scenes.md)** - Creating and managing lighting scenes

## Documentation Structure

```
docs/
├── README.md                 # This file
└── wiki/
    ├── README.md             # Wiki table of contents
    ├── quick-start.md        # Quick start guide
    ├── setup-guide.md        # Detailed setup instructions
    ├── configuration.md      # Configuration reference
    ├── integrations.md       # Lamp integration development
    ├── api-reference.md      # REST API documentation
    ├── events-and-effects.md # Game events and lighting effects
    ├── scenes.md             # Scenes and ambient lighting
    └── troubleshooting.md     # Common issues and solutions
```

## Building the Documentation

This documentation is written in Markdown and can be:

1. **Read directly on GitHub** - Markdown renders nicely in GitHub
2. **Viewed locally** - Any Markdown viewer works
3. **Hosted on a wiki platform** - Copy files to your wiki system
4. **Converted to HTML/PDF** - Use tools like `pandoc` or `mkdocs`

### Using mkdocs (Optional)

To build a static site from this documentation:

```bash
# Install mkdocs
pip install mkdocs mkdocs-material

# Create mkdocs.yml
cat > mkdocs.yml << 'EOF'
site_name: LumeHaven Documentation
theme:
  name: material
nav:
  - Home: README.md
  - Quick Start: wiki/quick-start.md
  - Setup Guide: wiki/setup-guide.md
  - Configuration: wiki/configuration.md
  - Integrations: wiki/integrations.md
  - API Reference: wiki/api-reference.md
  - Events & Effects: wiki/events-and-effects.md
  - Scenes: wiki/scenes.md
  - Troubleshooting: wiki/troubleshooting.md
EOF

# Build the site
mkdocs build

# Serve locally
mkdocs serve
```

Then open `http://localhost:8000` in your browser.

## Contributing to Documentation

Contributions to the documentation are welcome! Please:

1. Fork the repository
2. Make your changes in the `docs/wiki/` directory
3. Ensure links between documents are correct
4. Submit a pull request

## License

The documentation is licensed under the same license as the LumeHaven project itself. See the main [LICENSE](../../LICENSE) file for details.

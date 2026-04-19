# envchain

> CLI tool to manage and switch between named environment variable sets per project

---

## Installation

```bash
pip install envchain
```

---

## Usage

Create and manage named environment variable sets for your projects.

```bash
# Add a new environment set
envchain add myproject --env API_KEY=abc123 --env DB_URL=postgres://localhost/dev

# List all saved environments
envchain list

# Activate an environment set
envchain use myproject

# Show variables in a set
envchain show myproject

# Remove an environment set
envchain remove myproject
```

Switch between environments seamlessly when working across multiple projects:

```bash
# Load environment into current shell session
eval $(envchain use myproject)
```

---

## Commands

| Command | Description |
|---|---|
| `add <name>` | Create a new environment set |
| `use <name>` | Activate an environment set |
| `list` | List all saved environment sets |
| `show <name>` | Display variables in a set |
| `remove <name>` | Delete an environment set |

---

## License

MIT © [envchain contributors](LICENSE)
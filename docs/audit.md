# Audit Log

envchain records an audit log of operations performed on chains. This helps track changes and activations over time.

## Commands

### View the log

```bash
envchain audit log
```

Filter by chain name:

```bash
envchain audit log --chain prod
```

Filter by action type:

```bash
envchain audit log --action set
```

Limit output (default 50):

```bash
envchain audit log --limit 10
```

### Clear the log

```bash
envchain audit clear
```

You will be prompted to confirm before clearing.

### Show log file path

```bash
envchain audit path
```

## Log Format

Each entry is stored as a JSON line with the following fields:

| Field    | Description                        |
|----------|------------------------------------|
| `ts`     | ISO 8601 timestamp (UTC)           |
| `action` | Operation type (set, delete, etc.) |
| `chain`  | Chain name affected                |
| `detail` | Optional extra info (e.g. key)     |

## Log Location

The audit log is stored at:

```
~/.config/envchain/audit.log
```

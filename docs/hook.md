# Hook

The `hook` feature lets you attach shell commands to lifecycle events for a chain. These hooks can be used to trigger notifications, logging, or any side-effect when a chain is activated or deactivated.

## Events

| Event              | When it fires                        |
|--------------------|--------------------------------------|
| `pre_activate`     | Before a chain is activated          |
| `post_activate`    | After a chain is activated           |
| `pre_deactivate`   | Before a chain is deactivated        |
| `post_deactivate`  | After a chain is deactivated         |

## Commands

### Set a hook

```bash
envchain hook set <chain> <event> <command>
```

**Example:**
```bash
envchain hook set prod post_activate "echo Switched to prod"
```

### Remove a hook

```bash
envchain hook remove <chain> <event>
```

**Example:**
```bash
envchain hook remove prod post_activate
```

### Show a hook

```bash
envchain hook show <chain> <event>
```

### List all hooks for a chain

```bash
envchain hook list <chain>
```

**Example output:**
```
pre_activate: echo about to switch
post_activate: notify.sh prod
```

## Notes

- Hook commands are stored in the same store file as chains, keyed internally.
- Hooks are not executed automatically by envchain itself — they are intended to be invoked by your shell integration or wrapper scripts.
- Deleting a chain does not automatically remove its hooks; use `hook remove` explicitly if needed.

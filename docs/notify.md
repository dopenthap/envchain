# Notify

The `notify` feature lets you register shell commands (hooks) that fire when a chain is **activated** or **deactivated**.

This is useful for side-effects like logging, sending a Slack message, or updating a status file.

---

## Commands

### Set a hook

```bash
envchain notify set <chain> <event> <command>
```

`event` must be either `activate` or `deactivate`.

**Example:**
```bash
envchain notify set prod activate "echo switched to prod >> ~/.envchain.log"
```

---

### Remove a hook

```bash
envchain notify remove <chain> <event>
```

**Example:**
```bash
envchain notify remove prod activate
```

---

### Show hooks

Show all hooks for a chain:
```bash
envchain notify show <chain>
```

Show a specific event's hook:
```bash
envchain notify show <chain> <event>
```

**Example:**
```bash
envchain notify show prod
# activate: echo switched to prod >> ~/.envchain.log
# deactivate: echo left prod
```

---

## Notes

- Hooks are stored inside the envchain store file alongside the chain data.
- Only `activate` and `deactivate` events are supported.
- Hooks are plain shell strings — it is your responsibility to ensure they are safe.
- Hooks are **not** automatically executed by envchain itself; they are intended to be evaluated by the shell integration layer (e.g. `eval_snippet`).

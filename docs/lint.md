# envchain lint

The `lint` command inspects your chains for common issues that might indicate misconfiguration or security concerns.

## Usage

```bash
envchain lint [CHAINS...]
```

Run against all chains:

```bash
envchain lint
```

Or scope to specific chains:

```bash
envchain lint prod staging
```

## Checks

| Issue | Description |
|---|---|
| `empty value` | A key exists but has no value set |
| `key is not uppercase` | Convention is `ALL_CAPS` for env var names |
| `key contains spaces` | Spaces in key names will break most shells |
| `duplicate value shared across chains` | The same secret value appears in multiple chains — possible unintentional reuse |

## Exit codes

- `0` — no issues found
- `1` — one or more warnings were emitted

## Example output

```
[prod]
  api_key: key is not uppercase
  SECRET: duplicate value shared across chains

[staging]
  SECRET: duplicate value shared across chains
```

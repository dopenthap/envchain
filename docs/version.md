# Version Tracking

envchain can track a monotonically increasing version counter for each chain. This is useful for auditing change frequency or coordinating deployments.

## Commands

### Bump

Increment the version counter for a chain:

```bash
envchain version bump prod
# version: 1
```

Each call increments by one:

```bash
envchain version bump prod
# version: 2
```

### Get

Read the current version without changing it:

```bash
envchain version get prod
# 2
```

Chains that have never been bumped return `0`.

### Reset

Reset the counter back to zero:

```bash
envchain version reset prod
# version reset for 'prod'
```

### List

Show version numbers for all chains that have been bumped at least once:

```bash
envchain version list
# dev     3
# prod    2
# staging 1
```

## Notes

- Version numbers are stored inside the main envchain store file alongside chain data.
- Counters are per-chain and independent of each other.
- Resetting does not delete the chain or its variables — only the counter is cleared.
- Versions are integers starting at 0 and always increment by 1.

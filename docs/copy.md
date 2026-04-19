# Chain Copy & Rename

envchain lets you duplicate or rename existing chains without having to re-enter variables.

## Copy a chain

Create a new chain with the same variables as an existing one:

```bash
envchain copy dev staging
```

If the destination chain already exists, the command will fail. Use `--overwrite` to replace it:

```bash
envchain copy dev staging --overwrite
```

## Rename a chain

Rename a chain (equivalent to copy + delete):

```bash
envchain rename dev development
```

Same `--overwrite` flag applies if the destination already exists.

## Use cases

- Quickly create a `staging` environment based on `prod`
- Rename a chain after a project restructure
- Snapshot a chain before making changes: `envchain copy prod prod-backup`

## Notes

- Copy is a **deep clone** — changes to the destination won't affect the source.
- Both commands operate on the same local store as all other envchain commands.
- The source chain is **not** modified during a copy; it **is** removed during a rename.

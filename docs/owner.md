# Owner

The `owner` command lets you assign a human-readable owner string to any chain.
This is useful for auditing and governance — knowing who is responsible for a
given set of environment variables.

## Commands

### `envchain owner set <chain> <owner>`

Assign an owner to a chain.

```bash
envchain owner set prod alice
# Owner of 'prod' set to 'alice'.
```

### `envchain owner get <chain>`

Show the current owner of a chain.

```bash
envchain owner get prod
# alice
```

If no owner has been set:

```bash
envchain owner get dev
# No owner set for 'dev'.
```

### `envchain owner clear <chain>`

Remove the owner entry from a chain.

```bash
envchain owner clear prod
# Owner cleared for 'prod'.
```

### `envchain owner list`

List all chains that have an assigned owner.

```bash
envchain owner list
# dev     bob
# prod    alice
```

## Notes

- Owner strings are stored as chain metadata and do **not** appear when the
  chain is exported or activated.
- Setting an owner on a chain that does not exist raises an error.
- Calling `set` a second time overwrites the previous value.

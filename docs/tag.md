# Tag

The `tag` command lets you label chains with arbitrary tags for easier organization and filtering.

## Commands

### Add a tag

```bash
envchain tag add <chain> <tag>
```

Example:
```bash
envchain tag add prod production
envchain tag add prod aws
```

### Remove a tag

```bash
envchain tag remove <chain> <tag>
```

### List tags for a chain

```bash
envchain tag list <chain>
```

Output:
```
aws
production
```

### Find chains by tag

```bash
envchain tag find <tag>
```

Example:
```bash
envchain tag find aws
# dev
# prod
```

## Notes

- Tags are stored alongside your chains in the envchain store file.
- Tags are sorted alphabetically.
- Adding the same tag twice has no effect (deduplication is automatic).

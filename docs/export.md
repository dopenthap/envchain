# Exporting Environment Chains

The `export` command renders a named chain as shell-compatible export statements,
making it easy to source variables into your current shell session.

## Usage

```bash
envchain export <chain> [--format bash|fish|dotenv] [--prefix PREFIX]
```

## Formats

| Format   | Example output                  |
|----------|---------------------------------|
| `bash`   | `export KEY="value"`            |
| `fish`   | `set -x KEY "value"`            |
| `dotenv` | `KEY="value"`                   |

Default format is `bash`.

## Examples

### Bash (default)

```bash
$ envchain export myproject
export API_KEY="abc123"
export DEBUG="true"
```

Source directly into your shell:

```bash
eval $(envchain export myproject)
```

### Fish shell

```fish
envchain export myproject --format fish | source
```

### dotenv file

```bash
envchain export myproject --format dotenv > .env
```

### With a prefix

```bash
$ envchain export myproject --prefix MYAPP
export MYAPP_API_KEY="abc123"
export MYAPP_DEBUG="true"
```

## Notes

- Variable names are sorted alphabetically in the output.
- Special characters (`"` and `\`) in values are automatically escaped.

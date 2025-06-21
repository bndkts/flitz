# Configuration

## Configuration File

Flitz loads configuration from `~/.flitz.yml` in your home directory. If this file doesn't exist, default values are used.

## Configuration Options

### Basic Configuration

```yaml
# Font size for the application (default: 14)
font_size: 16

# External configuration files (optional)
external_config:
  - /path/to/additional/config.yml
  - /another/config/file.yml
```

### External Configuration

You can reference external configuration files that will be loaded and can override the main configuration:

```yaml
# ~/.flitz.yml
font_size: 14
external_config: /etc/flitz/company-config.yml
```

```yaml
# /etc/flitz/company-config.yml
font_size: 16  # This will override the main config
```

External configs are loaded in order and can partially override existing settings.

## Configuration Schema

The configuration is validated using Pydantic. Here's the complete schema:

### font_size
- **Type**: Integer
- **Default**: 14
- **Range**: 8-24 (enforced by the application)
- **Description**: Font size for the entire application interface

### external_config
- **Type**: String or List of Strings (optional)
- **Default**: None
- **Description**: Path(s) to additional configuration files

## Examples

### Minimal Configuration

```yaml
font_size: 18
```

### Advanced Configuration with External Files

```yaml
font_size: 14
external_config:
  - ~/.flitz-personal.yml
  - /shared/flitz-team.yml
```

### Personal Configuration Example

```yaml
# ~/.flitz-personal.yml
font_size: 16
```

### Team Configuration Example

```yaml
# /shared/flitz-team.yml
font_size: 12
```

## Configuration Loading Order

1. Load default values
2. Load main configuration from `~/.flitz.yml` (if exists)
3. Load external configurations in the order specified
4. Later configurations override earlier ones

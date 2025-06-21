# Flitz

A modern file explorer application built with Python and PyQt6.

## Features

- Modern list view with columns for Name, Size, Type, and Date Modified
- Navigate folders by double-clicking
- URL bar with current path and up button
- Adjustable font size with Ctrl +/-
- Sortable columns by clicking headers
- Command line support: `flitz /path/to/directory`
- Configuration via `~/.flitz.yml`
- File/folder operations: rename (F2), delete (Del), copy/cut/paste (Ctrl+C/X/V)
- Context menu with create folder/file, rename, and properties
- Search functionality (Ctrl+F)
- Toggle hidden files visibility (Ctrl+H)

## Installation

```bash
pip install flitz
```

## Usage

```bash
# Open current directory
flitz

# Open specific directory
flitz /path/to/directory
```

## Configuration

Create a configuration file at `~/.flitz.yml`:

```yaml
font_size: 16
external_config: /path/to/additional/config.yml
```

## Development

```bash
git clone https://github.com/bndkts/flitz.git
cd flitz
pip install -e ".[dev]"
pre-commit install
```

## Documentation

Documentation is available at [flitz.readthedocs.io](https://flitz.readthedocs.io).

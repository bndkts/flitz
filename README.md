# Flitz

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, feature-rich file explorer application built with Python and PyQt6. Flitz provides an intuitive interface for browsing and managing files with keyboard shortcuts, customizable settings, and powerful file operations.

![Flitz Screenshot](https://via.placeholder.com/800x500?text=Flitz+File+Explorer+Screenshot)

## ✨ Features

### 🗂️ **Modern Interface**
- Clean list view with sortable columns (Name, Size, Type, Date Modified)
- Responsive URL bar showing current path with navigation buttons
- Real-time search with instant filtering
- Context-sensitive right-click menus

### 🎯 **Navigation & Control**
- **Double-click** folders to navigate or files to open
- **Up button** for quick parent directory access
- **Command line support**: `flitz /path/to/directory`
- **Keyboard shortcuts** for all major operations

### ⚙️ **Customization**
- **Font size control** (Ctrl +/-) for better accessibility
- **Configuration file** support (`~/.flitz.yml`)
- **External config** loading for team/organizational settings
- **Hidden files toggle** (Ctrl+H)

### 📁 **File Operations**
- **Create** folders and files via context menu
- **Rename** items with F2
- **Delete** with confirmation (Del key)
- **Copy/Cut/Paste** operations (Ctrl+C/X/V)
- **Properties dialog** with detailed file information

### 🔍 **Search & Filter**
- **Real-time search** (Ctrl+F) with instant results
- **Smart filtering** of file and folder names
- **Escape to clear** search and restore full view

## 🚀 Installation

### From PyPI (Recommended)
```bash
pip install flitz
```

### From Source
```bash
git clone https://github.com/bndkts/flitz.git
cd flitz
pip install .
```

### Development Installation
```bash
git clone https://github.com/bndkts/flitz.git
cd flitz
pip install -e ".[dev]"
pre-commit install
```

## 📖 Usage

### Basic Usage
```bash
# Open current directory
flitz

# Open specific directory
flitz /path/to/directory

# Show help
flitz --help

# Show version
flitz --version
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl +` | Increase font size |
| `Ctrl -` | Decrease font size |
| `Ctrl F` | Open search bar |
| `Ctrl H` | Toggle hidden files |
| `Ctrl C` | Copy selected items |
| `Ctrl X` | Cut selected items |
| `Ctrl V` | Paste items |
| `F2` | Rename selected item |
| `Del` | Delete selected items |
| `Enter` | Open file/enter directory |
| `Esc` | Close search/context menu |

### Mouse Operations
- **Single-click**: Select item
- **Double-click**: Open file or enter directory
- **Right-click**: Show context menu
- **Column headers**: Click to sort by that column

## ⚙️ Configuration

Flitz uses a YAML configuration file located at `~/.flitz.yml`. Create this file to customize your experience:

```yaml
# Font size for the application interface
font_size: 16

# External configuration files (optional)
# These can override the main configuration
external_config:
  - /shared/team-flitz-config.yml
  - ~/.flitz-personal.yml
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `font_size` | integer | 14 | Application font size (8-24) |
| `external_config` | string/list | null | Path(s) to additional config files |

### External Configuration

External configurations allow for hierarchical settings management:

```yaml
# Company-wide settings (/shared/team-flitz-config.yml)
font_size: 12

# Personal overrides (~/.flitz-personal.yml)
font_size: 16  # Overrides company setting
```

## 🛠️ Development

### Project Structure
```
flitz/
├── flitz/              # Main package
│   ├── __init__.py     # Package initialization
│   ├── config.py       # Configuration management
│   ├── file_operations.py  # File system operations
│   └── main.py         # GUI application & entry point
├── tests/              # Test suite
├── docs/               # Sphinx documentation
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

### Prerequisites
- Python 3.9 or higher
- PyQt6
- See `pyproject.toml` for complete dependency list

### Setting Up Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bndkts/flitz.git
   cd flitz
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

4. **Run tests**:
   ```bash
   pytest
   ```

5. **Build documentation**:
   ```bash
   cd docs
   make html
   ```

### Code Quality

We maintain high code quality standards:

- **Black** for consistent code formatting
- **isort** for import organization
- **flake8** for linting and style checking
- **mypy** for static type checking
- **pytest** for comprehensive testing

Run all quality checks:
```bash
pre-commit run --all-files
```

### Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=flitz

# Run specific test file
pytest tests/test_config.py
```

## 📚 Documentation

- **User Guide**: [flitz.readthedocs.io](https://flitz.readthedocs.io)
- **API Reference**: [API Documentation](https://flitz.readthedocs.io/en/latest/api.html)
- **Contributing**: [Contributing Guide](https://flitz.readthedocs.io/en/latest/contributing.html)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Requirements

- **Python**: 3.9 or higher
- **PyQt6**: 6.4.0 or higher
- **pydantic**: 2.0.0 or higher
- **PyYAML**: 6.0 or higher

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Bug Reports & Feature Requests

- **Bug Reports**: [GitHub Issues](https://github.com/bndkts/flitz/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/bndkts/flitz/discussions)
- **Security Issues**: Email [security@flitz-project.org](mailto:security@flitz-project.org)

## 🎯 Roadmap

- [ ] **Plugin System**: Support for custom file type handlers
- [ ] **Themes**: Light/dark mode and custom color schemes
- [ ] **Network Support**: FTP/SFTP remote file browsing
- [ ] **Advanced Search**: Regular expressions and content search
- [ ] **File Preview**: Quick preview panel for common file types
- [ ] **Bookmarks**: Save and manage favorite directories

## 🙏 Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- Configuration management powered by [Pydantic](https://pydantic-docs.helpmanual.io/)
- Documentation built with [Sphinx](https://www.sphinx-doc.org/)
- Packaging handled by [Flit](https://flit.pypa.io/)

---

**Made with ❤️ by the Flitz Team**
```

## Documentation

Documentation is available at [flitz.readthedocs.io](https://flitz.readthedocs.io).

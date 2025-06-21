"""Tests for configuration management."""

import tempfile
from pathlib import Path

import yaml

from flitz.config import Config


def test_default_config():
    """Test default configuration values."""
    config = Config()
    assert config.font_size == 14
    assert config.external_config is None


def test_load_config_nonexistent_file(monkeypatch):
    """Test loading config when file doesn't exist."""
    # Mock Path.home() to return a non-existent directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        fake_home = Path(tmp_dir) / "fake_home"
        monkeypatch.setattr(Path, "home", lambda: fake_home)

        config = Config.load()
        assert config.font_size == 14
        assert config.external_config is None


def test_load_config_existing_file(monkeypatch):
    """Test loading config from existing file."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        fake_home = Path(tmp_dir)
        config_path = fake_home / ".flitz.yml"

        # Create config file
        config_data = {"font_size": 18}
        with open(config_path, "w") as f:
            yaml.dump(config_data, f)

        monkeypatch.setattr(Path, "home", lambda: fake_home)

        config = Config.load()
        assert config.font_size == 18


def test_load_config_with_external_config(monkeypatch):
    """Test loading config with external configuration."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        fake_home = Path(tmp_dir)
        config_path = fake_home / ".flitz.yml"
        external_config_path = fake_home / "external.yml"

        # Create external config
        external_data = {"font_size": 20}
        with open(external_config_path, "w") as f:
            yaml.dump(external_data, f)

        # Create main config referencing external
        main_data = {
            "font_size": 16,
            "external_config": [str(external_config_path)],
        }
        with open(config_path, "w") as f:
            yaml.dump(main_data, f)

        monkeypatch.setattr(Path, "home", lambda: fake_home)

        config = Config.load()
        # External config should override main config
        assert config.font_size == 20


def test_config_validation():
    """Test configuration validation."""
    # Valid config
    config = Config(font_size=16)
    assert config.font_size == 16

    # Test with external_config as string (should be converted to list)
    config = Config(font_size=14, external_config="path/to/config")
    assert config.external_config == ["path/to/config"]

    # Test with external_config as list
    config = Config(font_size=14, external_config=["path1", "path2"])
    assert config.external_config == ["path1", "path2"]

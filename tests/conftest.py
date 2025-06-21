"""Test fixtures for Flitz tests."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files and directories for testing."""
    # Create test directory structure
    (temp_dir / "folder1").mkdir()
    (temp_dir / "folder2").mkdir()
    (temp_dir / ".hidden_folder").mkdir()

    # Create test files
    (temp_dir / "file1.txt").write_text("Hello, world!")
    (temp_dir / "file2.py").write_text("print('Hello')")
    (temp_dir / ".hidden_file").write_text("Hidden content")
    (temp_dir / "folder1" / "nested_file.md").write_text("# Nested file")

    return temp_dir


@pytest.fixture
def config_file(temp_dir):
    """Create a temporary config file."""
    config_path = temp_dir / "test_config.yml"
    config_content = """
font_size: 16
external_config: []
"""
    config_path.write_text(config_content)
    return config_path

"""Tests for file operations."""

from flitz.file_operations import FileItem, FileOperations


def test_file_item_properties(sample_files):
    """Test FileItem properties."""
    file_path = sample_files / "file1.txt"
    item = FileItem(file_path)

    assert item.name == "file1.txt"
    assert item.size > 0
    assert item.size_str.endswith("B")
    assert not item.is_directory
    assert not item.is_hidden
    assert item.file_type == "Text Document"
    assert item.modified_str  # Should have a modification time


def test_file_item_directory(sample_files):
    """Test FileItem for directory."""
    dir_path = sample_files / "folder1"
    item = FileItem(dir_path)

    assert item.name == "folder1"
    assert item.size == 0
    assert item.size_str == ""
    assert item.is_directory
    assert not item.is_hidden
    assert item.file_type == "Folder"


def test_file_item_hidden(sample_files):
    """Test FileItem for hidden file."""
    hidden_path = sample_files / ".hidden_file"
    item = FileItem(hidden_path)

    assert item.is_hidden


def test_file_item_size_formatting():
    """Test file size formatting."""

    # Mock a large file
    class MockPath:
        def __init__(self, size):
            self._size = size
            self.name = "test"
            self.suffix = ""

        def is_dir(self):
            return False

        def stat(self):
            class MockStat:
                def __init__(self, size):
                    self.st_size = size
                    self.st_mtime = 1234567890

            return MockStat(self._size)

    # Test different size ranges
    item = FileItem.__new__(FileItem)
    item.path = MockPath(1024)
    item._stat = None
    assert "1.0 KB" in item.size_str

    item.path = MockPath(1024 * 1024)
    item._stat = None
    assert "1.0 MB" in item.size_str


def test_list_directory(sample_files):
    """Test directory listing."""
    items = FileOperations.list_directory(sample_files, show_hidden=False)

    # Should not include hidden files
    names = [item.name for item in items]
    assert "file1.txt" in names
    assert "folder1" in names
    assert ".hidden_file" not in names
    assert ".hidden_folder" not in names


def test_list_directory_with_hidden(sample_files):
    """Test directory listing with hidden files."""
    items = FileOperations.list_directory(sample_files, show_hidden=True)

    # Should include hidden files
    names = [item.name for item in items]
    assert "file1.txt" in names
    assert ".hidden_file" in names
    assert ".hidden_folder" in names


def test_can_access(sample_files):
    """Test access checking."""
    assert FileOperations.can_access(sample_files)
    assert FileOperations.can_access(sample_files / "file1.txt")
    assert not FileOperations.can_access(sample_files / "nonexistent")


def test_create_folder(sample_files):
    """Test folder creation."""
    assert FileOperations.create_folder(sample_files, "new_folder")
    assert (sample_files / "new_folder").is_dir()

    # Test creating duplicate folder
    assert not FileOperations.create_folder(sample_files, "new_folder")


def test_create_file(sample_files):
    """Test file creation."""
    assert FileOperations.create_file(sample_files, "new_file.txt")
    assert (sample_files / "new_file.txt").is_file()

    # Test creating duplicate file
    assert not FileOperations.create_file(sample_files, "new_file.txt")


def test_rename_item(sample_files):
    """Test item renaming."""
    old_path = sample_files / "file1.txt"
    assert FileOperations.rename_item(old_path, "renamed_file.txt")
    assert not old_path.exists()
    assert (sample_files / "renamed_file.txt").exists()


def test_delete_item(sample_files):
    """Test item deletion."""
    file_path = sample_files / "file1.txt"
    assert FileOperations.delete_item(file_path)
    assert not file_path.exists()

    # Test deleting directory
    dir_path = sample_files / "folder1"
    assert FileOperations.delete_item(dir_path)
    assert not dir_path.exists()


def test_copy_item(sample_files, temp_dir):
    """Test item copying."""
    src = sample_files / "file1.txt"
    dst = temp_dir / "copied_file.txt"

    assert FileOperations.copy_item(src, dst)
    assert src.exists()  # Original should still exist
    assert dst.exists()
    assert src.read_text() == dst.read_text()


def test_move_item(sample_files, temp_dir):
    """Test item moving."""
    src = sample_files / "file1.txt"
    dst = temp_dir / "moved_file.txt"
    original_content = src.read_text()

    assert FileOperations.move_item(src, dst)
    assert not src.exists()  # Original should be gone
    assert dst.exists()
    assert dst.read_text() == original_content

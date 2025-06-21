"""File operations and utilities."""

import os
import shutil
from pathlib import Path
from typing import Any, List, Optional

from PyQt6.QtCore import QDateTime
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyle


class FileItem:
    """Represents a file or directory item."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._stat: Optional[Any] = None

    @property
    def stat(self) -> Optional[Any]:
        """Cached file statistics."""
        if self._stat is None:
            try:
                self._stat = self.path.stat()
            except (OSError, PermissionError):
                self._stat = None
        return self._stat

    @property
    def name(self) -> str:
        """File/directory name."""
        return self.path.name

    @property
    def size(self) -> int:
        """File size in bytes."""
        if self.is_directory or self.stat is None:
            return 0
        return int(self.stat.st_size)

    @property
    def size_str(self) -> str:
        """Human-readable file size."""
        if self.is_directory:
            return ""

        size = float(self.size)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    @property
    def is_directory(self) -> bool:
        """Check if item is a directory."""
        return self.path.is_dir()

    @property
    def is_hidden(self) -> bool:
        """Check if item is hidden."""
        return self.name.startswith(".")

    @property
    def file_type(self) -> str:
        """File type description."""
        if self.is_directory:
            return "Folder"

        suffix = self.path.suffix.lower()
        if not suffix:
            return "File"

        type_map = {
            ".txt": "Text Document",
            ".py": "Python Script",
            ".js": "JavaScript File",
            ".html": "HTML Document",
            ".css": "CSS Stylesheet",
            ".json": "JSON File",
            ".xml": "XML Document",
            ".pdf": "PDF Document",
            ".jpg": "JPEG Image",
            ".jpeg": "JPEG Image",
            ".png": "PNG Image",
            ".gif": "GIF Image",
            ".svg": "SVG Image",
            ".mp3": "MP3 Audio",
            ".mp4": "MP4 Video",
            ".zip": "ZIP Archive",
            ".tar": "TAR Archive",
            ".gz": "GZIP Archive",
        }

        return type_map.get(suffix, f"{suffix[1:].upper()} File")

    @property
    def modified_time(self) -> QDateTime:
        """Last modified time."""
        if self.stat is None:
            return QDateTime()
        return QDateTime.fromSecsSinceEpoch(int(self.stat.st_mtime))

    @property
    def modified_str(self) -> str:
        """Human-readable modified time."""
        return str(self.modified_time.toString("yyyy-MM-dd hh:mm:ss"))

    def get_icon(self, style: QStyle) -> QIcon:
        """Get appropriate icon for the file type."""
        if self.is_directory:
            return style.standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        else:
            return style.standardIcon(QStyle.StandardPixmap.SP_FileIcon)


class FileOperations:
    """File operations utilities."""

    @staticmethod
    def list_directory(
        path: Path, show_hidden: bool = False
    ) -> List[FileItem]:
        """List directory contents."""
        items = []
        try:
            for item_path in path.iterdir():
                item = FileItem(item_path)
                if not show_hidden and item.is_hidden:
                    continue
                items.append(item)
        except (OSError, PermissionError):
            pass
        return items

    @staticmethod
    def can_access(path: Path) -> bool:
        """Check if path is accessible."""
        try:
            return path.exists() and os.access(path, os.R_OK)
        except (OSError, PermissionError):
            return False

    @staticmethod
    def create_folder(parent: Path, name: str) -> bool:
        """Create a new folder."""
        try:
            new_path = parent / name
            new_path.mkdir(exist_ok=False)
            return True
        except (OSError, PermissionError, FileExistsError):
            return False

    @staticmethod
    def create_file(parent: Path, name: str) -> bool:
        """Create a new empty file."""
        try:
            new_path = parent / name
            new_path.touch(exist_ok=False)
            return True
        except (OSError, PermissionError, FileExistsError):
            return False

    @staticmethod
    def rename_item(old_path: Path, new_name: str) -> bool:
        """Rename a file or directory."""
        try:
            new_path = old_path.parent / new_name
            old_path.rename(new_path)
            return True
        except (OSError, PermissionError, FileExistsError):
            return False

    @staticmethod
    def delete_item(path: Path) -> bool:
        """Delete a file or directory."""
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            return True
        except (OSError, PermissionError):
            return False

    @staticmethod
    def copy_item(src: Path, dst: Path) -> bool:
        """Copy a file or directory."""
        try:
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return True
        except (OSError, PermissionError, FileExistsError):
            return False

    @staticmethod
    def move_item(src: Path, dst: Path) -> bool:
        """Move a file or directory."""
        try:
            shutil.move(str(src), str(dst))
            return True
        except (OSError, PermissionError, FileExistsError):
            return False

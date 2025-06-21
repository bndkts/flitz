"""Main application and GUI components."""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from PyQt6.QtCore import QPoint, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QKeyEvent, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .config import Config
from .file_operations import FileItem, FileOperations


class SearchBar(QWidget):
    """Search bar widget."""

    search_requested = pyqtSignal(str)
    escape_pressed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()
        self.hide()

    def setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files and folders...")
        self.search_input.textChanged.connect(self.on_text_changed)
        self.search_input.returnPressed.connect(self.on_search)

        layout.addWidget(QLabel("Search:"))
        layout.addWidget(self.search_input)

    def keyPressEvent(self, event: Optional[QKeyEvent]) -> None:
        if event is None:
            return
        if event.key() == Qt.Key.Key_Escape:
            self.escape_pressed.emit()
        else:
            super().keyPressEvent(event)

    def on_text_changed(self, text: str) -> None:
        # Real-time search with a small delay
        if hasattr(self, "_search_timer"):
            self._search_timer.stop()

        self._search_timer: QTimer = QTimer()
        self._search_timer.timeout.connect(
            lambda: self.search_requested.emit(text)
        )
        self._search_timer.setSingleShot(True)
        self._search_timer.start(300)  # 300ms delay

    def on_search(self) -> None:
        self.search_requested.emit(self.search_input.text())

    def show_search(self) -> None:
        self.show()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def hide_search(self) -> None:
        self.hide()
        self.search_input.clear()


class FileListWidget(QTreeWidget):
    """Custom tree widget for file listing."""

    path_changed = pyqtSignal(Path)
    item_renamed = pyqtSignal(Path, str)

    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()
        self.current_path = Path.home()
        self.show_hidden = False
        self.clipboard_items: List[Path] = []
        self.clipboard_operation: Optional[str] = None  # 'copy' or 'cut'

    def setup_ui(self) -> None:
        self.setHeaderLabels(["Name", "Size", "Type", "Date Modified"])
        self.setRootIsDecorated(False)
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # Enable sorting
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        # Connect signals
        self.itemDoubleClicked.connect(self.on_item_double_clicked)

        # Adjust column widths
        header = self.header()
        if header is not None:
            header.setStretchLastSection(False)
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(
                1, QHeaderView.ResizeMode.ResizeToContents
            )
            header.setSectionResizeMode(
                2, QHeaderView.ResizeMode.ResizeToContents
            )
            header.setSectionResizeMode(
                3, QHeaderView.ResizeMode.ResizeToContents
            )

    def load_directory(self, path: Path) -> None:
        """Load directory contents into the tree widget."""
        if not FileOperations.can_access(path):
            QMessageBox.warning(
                self, "Access Denied", f"Cannot access: {path}"
            )
            return

        self.current_path = path
        self.clear()

        items = FileOperations.list_directory(path, self.show_hidden)

        # Sort: directories first, then files
        items.sort(key=lambda x: (not x.is_directory, x.name.lower()))

        for file_item in items:
            tree_item = QTreeWidgetItem(
                [
                    file_item.name,
                    file_item.size_str,
                    file_item.file_type,
                    file_item.modified_str,
                ]
            )
            style = self.style()
            if style is not None:
                tree_item.setIcon(0, file_item.get_icon(style))
            tree_item.setData(0, Qt.ItemDataRole.UserRole, file_item.path)
            self.addTopLevelItem(tree_item)

        self.path_changed.emit(path)

    def on_item_double_clicked(
        self, item: QTreeWidgetItem, column: int
    ) -> None:
        """Handle double-click on item."""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)

        if file_path.is_dir():
            self.load_directory(file_path)
        else:
            self.open_file(file_path)

    def open_file(self, file_path: Path) -> None:
        """Open file with default application."""
        try:
            if sys.platform == "win32":
                subprocess.run(
                    ["start", str(file_path)], shell=True, check=True
                )
            elif sys.platform == "darwin":
                subprocess.run(["open", str(file_path)], check=True)
            else:
                subprocess.run(["xdg-open", str(file_path)], check=True)
        except subprocess.CalledProcessError:
            QMessageBox.warning(self, "Error", f"Could not open: {file_path}")

    def keyPressEvent(self, event: Optional[QKeyEvent]) -> None:
        if event is None:
            return
        if event.key() == Qt.Key.Key_F2:
            self.rename_selected()
        elif event.key() == Qt.Key.Key_Delete:
            self.delete_selected()
        elif (
            event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter
        ):
            current = self.currentItem()
            if current:
                self.on_item_double_clicked(current, 0)
        elif event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selected()
        elif event.matches(QKeySequence.StandardKey.Cut):
            self.cut_selected()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_selected()
        else:
            super().keyPressEvent(event)

    def show_context_menu(self, position: QPoint) -> None:
        """Show context menu."""
        menu = QMenu(self)

        create_folder_action = QAction("Create Folder", self)
        create_folder_action.triggered.connect(self.create_folder)
        menu.addAction(create_folder_action)

        create_file_action = QAction("Create Empty File", self)
        create_file_action.triggered.connect(self.create_file)
        menu.addAction(create_file_action)

        menu.addSeparator()

        item = self.itemAt(position)
        if item:
            rename_action = QAction("Rename...", self)
            rename_action.triggered.connect(self.rename_selected)
            menu.addAction(rename_action)

            menu.addSeparator()

            properties_action = QAction("Properties", self)
            properties_action.triggered.connect(self.show_properties)
            menu.addAction(properties_action)

        menu.exec(self.mapToGlobal(position))

    def create_folder(self) -> None:
        """Create new folder."""
        name, ok = QInputDialog.getText(self, "Create Folder", "Folder name:")
        if ok and name:
            if FileOperations.create_folder(self.current_path, name):
                self.load_directory(self.current_path)
            else:
                QMessageBox.warning(
                    self, "Error", f"Could not create folder: {name}"
                )

    def create_file(self) -> None:
        """Create new empty file."""
        name, ok = QInputDialog.getText(self, "Create File", "File name:")
        if ok and name:
            if FileOperations.create_file(self.current_path, name):
                self.load_directory(self.current_path)
            else:
                QMessageBox.warning(
                    self, "Error", f"Could not create file: {name}"
                )

    def rename_selected(self) -> None:
        """Rename selected item."""
        item = self.currentItem()
        if not item:
            return

        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        current_name = file_path.name

        new_name, ok = QInputDialog.getText(
            self, "Rename", "New name:", text=current_name
        )
        if ok and new_name and new_name != current_name:
            if FileOperations.rename_item(file_path, new_name):
                self.load_directory(self.current_path)
                self.item_renamed.emit(file_path, new_name)
            else:
                QMessageBox.warning(
                    self, "Error", f"Could not rename to: {new_name}"
                )

    def delete_selected(self) -> None:
        """Delete selected items."""
        selected_items = self.selectedItems()
        if not selected_items:
            return

        file_names = [item.text(0) for item in selected_items]
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete {len(file_names)} item(s)?\\n\\n"
            + "\\n".join(file_names[:5])
            + ("\\n..." if len(file_names) > 5 else ""),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            success_count = 0
            for item in selected_items:
                file_path = item.data(0, Qt.ItemDataRole.UserRole)
                if FileOperations.delete_item(file_path):
                    success_count += 1

            self.load_directory(self.current_path)

            if success_count < len(selected_items):
                QMessageBox.warning(
                    self,
                    "Partial Success",
                    f"Deleted {success_count} of {len(selected_items)} items.",
                )

    def copy_selected(self) -> None:
        """Copy selected items to clipboard."""
        selected_items = self.selectedItems()
        self.clipboard_items = [
            item.data(0, Qt.ItemDataRole.UserRole) for item in selected_items
        ]
        self.clipboard_operation = "copy"

    def cut_selected(self) -> None:
        """Cut selected items to clipboard."""
        selected_items = self.selectedItems()
        self.clipboard_items = [
            item.data(0, Qt.ItemDataRole.UserRole) for item in selected_items
        ]
        self.clipboard_operation = "cut"

    def paste_selected(self) -> None:
        """Paste items from clipboard."""
        if not self.clipboard_items:
            return

        success_count = 0
        for src_path in self.clipboard_items:
            dst_path = self.current_path / src_path.name

            if self.clipboard_operation == "copy":
                if FileOperations.copy_item(src_path, dst_path):
                    success_count += 1
            elif self.clipboard_operation == "cut":
                if FileOperations.move_item(src_path, dst_path):
                    success_count += 1

        if self.clipboard_operation == "cut":
            self.clipboard_items.clear()

        self.load_directory(self.current_path)

        if success_count < len(self.clipboard_items):
            QMessageBox.warning(
                self,
                "Partial Success",
                f"Processed {success_count} of "
                f"{len(self.clipboard_items)} items.",
            )

    def show_properties(self) -> None:
        """Show properties dialog for selected item."""
        item = self.currentItem()
        if not item:
            return

        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        file_item = FileItem(file_path)

        info = f"""Path: {file_path}
Name: {file_item.name}
Type: {file_item.file_type}
Size: {file_item.size_str} ({file_item.size} bytes)
Modified: {file_item.modified_str}
Hidden: {"Yes" if file_item.is_hidden else "No"}"""

        QMessageBox.information(self, "Properties", info)

    def filter_items(self, search_text: str) -> None:
        """Filter items based on search text."""
        if not search_text:
            # Show all items
            for i in range(self.topLevelItemCount()):
                item = self.topLevelItem(i)
                if item is not None:
                    item.setHidden(False)
            return

        search_lower = search_text.lower()
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item is not None:
                name = item.text(0).lower()
                item.setHidden(search_lower not in name)

    def toggle_hidden_files(self) -> None:
        """Toggle visibility of hidden files."""
        self.show_hidden = not self.show_hidden
        self.load_directory(self.current_path)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.config = Config.load()
        self.setup_ui()
        self.setup_actions()
        self.apply_config()

    def setup_ui(self) -> None:
        self.setWindowTitle("Flitz File Explorer")
        self.setGeometry(100, 100, 1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Up button
        self.up_button = QPushButton()
        style = self.style()
        if style is not None:
            self.up_button.setIcon(
                style.standardIcon(style.StandardPixmap.SP_ArrowUp)
            )
        self.up_button.setToolTip("Go up one level")
        self.up_button.clicked.connect(self.go_up)
        self.toolbar.addWidget(self.up_button)

        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setReadOnly(True)
        self.toolbar.addWidget(self.address_bar)

        # Search bar
        self.search_bar = SearchBar()
        self.search_bar.search_requested.connect(self.on_search)
        self.search_bar.escape_pressed.connect(self.on_search_escape)
        layout.addWidget(self.search_bar)

        # File list
        self.file_list = FileListWidget()
        self.file_list.path_changed.connect(self.on_path_changed)
        layout.addWidget(self.file_list)

    def setup_actions(self) -> None:
        """Setup keyboard shortcuts and actions."""
        # Font size actions
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)
        self.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)
        self.addAction(zoom_out_action)

        # Search action
        search_action = QAction("Search", self)
        search_action.setShortcut(QKeySequence.StandardKey.Find)
        search_action.triggered.connect(self.show_search)
        self.addAction(search_action)

        # Toggle hidden files
        toggle_hidden_action = QAction("Toggle Hidden Files", self)
        toggle_hidden_action.setShortcut(QKeySequence("Ctrl+H"))
        toggle_hidden_action.triggered.connect(
            self.file_list.toggle_hidden_files
        )
        self.addAction(toggle_hidden_action)

    def apply_config(self) -> None:
        """Apply configuration settings."""
        font = self.font()
        font.setPointSize(self.config.font_size)
        self.setFont(font)

    def keyPressEvent(self, event: Optional[QKeyEvent]) -> None:
        if event is None:
            return
        if event.key() == Qt.Key.Key_Escape:
            if self.search_bar.isVisible():
                self.search_bar.hide_search()
            # Add context menu handling here if needed
        else:
            super().keyPressEvent(event)

    def zoom_in(self) -> None:
        """Increase font size."""
        self.config.font_size = min(self.config.font_size + 1, 24)
        self.apply_config()

    def zoom_out(self) -> None:
        """Decrease font size."""
        self.config.font_size = max(self.config.font_size - 1, 8)
        self.apply_config()

    def show_search(self) -> None:
        """Show search bar."""
        self.search_bar.show_search()

    def on_search(self, text: str) -> None:
        """Handle search request."""
        self.file_list.filter_items(text)

    def on_search_escape(self) -> None:
        """Handle escape in search bar."""
        self.search_bar.hide_search()
        self.file_list.filter_items("")  # Clear filter

    def go_up(self) -> None:
        """Go up one directory level."""
        parent = self.file_list.current_path.parent
        if parent != self.file_list.current_path:
            self.file_list.load_directory(parent)

    def on_path_changed(self, path: Path) -> None:
        """Handle path change."""
        self.address_bar.setText(str(path))
        self.up_button.setEnabled(path.parent != path)

    def navigate_to(self, path: Path) -> None:
        """Navigate to specified path."""
        if path.exists() and path.is_dir():
            self.file_list.load_directory(path)
        else:
            QMessageBox.warning(self, "Error", f"Invalid path: {path}")


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Flitz - A modern file explorer"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to open (default: current directory)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Flitz {__import__('flitz').__version__}",
    )

    args = parser.parse_args()

    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Flitz")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("Flitz Project")

    # Create main window
    window = MainWindow()

    # Handle path argument
    start_path = Path(args.path).resolve()
    window.navigate_to(start_path)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

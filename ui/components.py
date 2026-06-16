import os
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QSize
from PySide6.QtGui import QColor, QIcon

class DragDropZone(QFrame):
    paths_dropped = Signal(list)
    
    def __init__(self, supported_extensions=None, instruction_text="Drag & Drop files or folders here", parent=None):
        super().__init__(parent)
        self.supported_extensions = supported_extensions or []
        self.instruction_text = instruction_text
        
        self.setObjectName("DragDropZone")
        self.setProperty("class", "DragDropZone")
        self.setProperty("dragActive", False)
        self.setAcceptDrops(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(6)
        
        self.icon_label = QLabel("📥")
        self.icon_label.setStyleSheet("font-size: 24px; background: transparent; color: #FF4F00;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        self.main_label = QLabel(self.instruction_text)
        self.main_label.setProperty("class", "DragDropLabel")
        self.main_label.setAlignment(Qt.AlignCenter)
        
        ext_list = ", ".join(self.supported_extensions).replace(".", "").upper()
        subtext = f"Supports: {ext_list} and Folders" if self.supported_extensions else "Supports Files and Folders"
        self.sub_label = QLabel(subtext)
        self.sub_label.setProperty("class", "DragDropSublabel")
        self.sub_label.setAlignment(Qt.AlignCenter)
        
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(12)
        btn_layout.setContentsMargins(0, 8, 0, 0)
        
        self.browse_file_btn = QPushButton("Select Files")
        self.browse_file_btn.setProperty("class", "SecondaryBtn")
        self.browse_file_btn.setCursor(Qt.PointingHandCursor)
        self.browse_file_btn.setMinimumHeight(32)
        self.browse_file_btn.clicked.connect(self.browse_files)
        
        self.browse_folder_btn = QPushButton("Select Folder")
        self.browse_folder_btn.setProperty("class", "SecondaryBtn")
        self.browse_folder_btn.setCursor(Qt.PointingHandCursor)
        self.browse_folder_btn.setMinimumHeight(32)
        self.browse_folder_btn.clicked.connect(self.browse_folder)
        
        btn_layout.addWidget(self.browse_file_btn)
        btn_layout.addWidget(self.browse_folder_btn)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.main_label)
        layout.addWidget(self.sub_label)
        layout.addLayout(btn_layout)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", True)
            self.style().polish(self)
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dragLeaveEvent(self, event):
        self.setProperty("dragActive", False)
        self.style().polish(self)
        
    def dropEvent(self, event):
        self.setProperty("dragActive", False)
        self.style().polish(self)
        
        urls = event.mimeData().urls()
        if urls:
            dropped_paths = []
            for url in urls:
                path = url.toLocalFile()
                if os.path.exists(path):
                    dropped_paths.append(path)
            if dropped_paths:
                self.paths_dropped.emit(dropped_paths)
                        
    def browse_files(self):
        filt = ""
        if self.supported_extensions:
            ext_filters = " ".join([f"*{ext}" for ext in self.supported_extensions])
            filt = f"Supported Files ({ext_filters});;All Files (*)"
        else:
            filt = "All Files (*)"
            
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", filt)
        if file_paths:
            self.paths_dropped.emit(file_paths)
            
    def browse_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", "")
        if dir_path:
            self.paths_dropped.emit([dir_path])

class FileListItemWidget(QWidget):
    removed = Signal(str)
    
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(10)
        
        is_dir = os.path.isdir(file_path)
        icon_lbl = QLabel("📁" if is_dir else "📄")
        icon_lbl.setStyleSheet("font-size: 15px; color: #FF4F00; background: transparent;")
        
        name_lbl = QLabel(os.path.basename(file_path))
        name_lbl.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 13px; background: transparent;")
        
        size_str = ""
        if not is_dir:
            try:
                size_kb = os.path.getsize(file_path) / 1024
                if size_kb > 1024:
                    size_str = f"({size_kb/1024:.1f} MB)"
                else:
                    size_str = f"({size_kb:.1f} KB)"
            except Exception:
                pass
        else:
            size_str = "(Folder)"
            
        size_lbl = QLabel(size_str)
        size_lbl.setStyleSheet("color: #8E8E93; font-size: 11px; background: transparent;")
        
        path_lbl = QLabel(os.path.dirname(file_path))
        path_lbl.setStyleSheet("color: #636366; font-size: 11px; background: transparent;")
        path_lbl.setElideMode(Qt.ElideLeft)
        
        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(22, 22)
        remove_btn.setStyleSheet("""
            QPushButton {
                color: #8E8E93;
                font-weight: bold;
                background-color: transparent;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                color: #FF453A;
            }
        """)
        remove_btn.setCursor(Qt.PointingHandCursor)
        remove_btn.clicked.connect(lambda: self.removed.emit(self.file_path))
        
        layout.addWidget(icon_lbl)
        layout.addWidget(name_lbl)
        layout.addWidget(size_lbl)
        layout.addWidget(path_lbl, 1)
        layout.addWidget(remove_btn)

class SelectedFilesList(QWidget):
    list_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_paths = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        self.header_lbl = QLabel("Selected Assets (0)")
        self.header_lbl.setStyleSheet("font-weight: 700; color: #FFFFFF; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;")
        
        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(120)
        self.list_widget.setMaximumHeight(200)
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        
        layout.addWidget(self.header_lbl)
        layout.addWidget(self.list_widget)
        
    def add_paths(self, paths):
        for p in paths:
            if p not in self.file_paths:
                self.file_paths.append(p)
                
                item = QListWidgetItem(self.list_widget)
                widget = FileListItemWidget(p)
                widget.removed.connect(self.remove_path)
                
                item.setSizeHint(QSize(100, 36))
                self.list_widget.addItem(item)
                self.list_widget.setItemWidget(item, widget)
                
        self.update_header()
        self.list_changed.emit()
        
    def remove_path(self, path):
        if path in self.file_paths:
            idx = self.file_paths.index(path)
            self.file_paths.remove(path)
            item = self.list_widget.takeItem(idx)
            del item
            
            self.update_header()
            self.list_changed.emit()
            
    def clear(self):
        self.file_paths.clear()
        self.list_widget.clear()
        self.update_header()
        self.list_changed.emit()
        
    def update_header(self):
        self.header_lbl.setText(f"Selected Assets ({len(self.file_paths)})")
        
    def get_paths(self):
        return self.file_paths

class GlowButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor("#FF4F00")) # Vermillion Orange glow
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        self.anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim.setDuration(220)
        self.setMinimumHeight(38)
        
    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.shadow.blurRadius())
        self.anim.setEndValue(12)
        self.anim.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.shadow.blurRadius())
        self.anim.setEndValue(0)
        self.anim.start()
        super().leaveEvent(event)

class CollapsibleSection(QWidget):
    def __init__(self, title="Advanced Settings", parent=None):
        super().__init__(parent)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.header_button = QPushButton(title)
        self.header_button.setProperty("class", "CollapseHeader")
        self.header_button.setCursor(Qt.PointingHandCursor)
        self.header_button.setCheckable(True)
        self.header_button.setChecked(False)
        self.header_button.setMinimumHeight(38)
        self.header_button.clicked.connect(self.toggle_collapse)
        
        self.content_frame = QFrame()
        self.content_frame.setProperty("class", "CardFrame")
        self.content_frame.setStyleSheet("border-top: none; border-top-left-radius: 0px; border-top-right-radius: 0px; margin-bottom: 0px;")
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(12)
        
        self.main_layout.addWidget(self.header_button)
        self.main_layout.addWidget(self.content_frame)
        
        self.content_frame.setVisible(False)
        self.update_arrow()
        
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)
        
    def add_layout(self, layout):
        self.content_layout.addLayout(layout)
        
    def toggle_collapse(self):
        checked = self.header_button.isChecked()
        self.content_frame.setVisible(checked)
        if checked:
            self.header_button.setStyleSheet("text-align: left; padding: 12px; font-weight: bold; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;")
        else:
            self.header_button.setStyleSheet("text-align: left; padding: 12px; font-weight: bold;")
        self.update_arrow()
        
    def update_arrow(self):
        arrow = "▼" if self.header_button.isChecked() else "▶"
        title_text = self.header_button.text().lstrip("▶ ").lstrip("▼ ")
        self.header_button.setText(f"{arrow}  {title_text}")

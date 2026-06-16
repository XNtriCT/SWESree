import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QProgressBar, QTextEdit, QSlider, QCheckBox, QMessageBox, QLineEdit, QScrollArea
from PySide6.QtCore import Qt, Signal
from ui.components import DragDropZone, CollapsibleSection, SelectedFilesList, GlowButton
from workers.frame_worker import FrameWorker

class FramesToolView(QWidget):
    stats_updated = Signal(int, float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        # 1. Main outer layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 2. Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 3. Content container widget
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(20)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        title = QLabel("Video → Frames Extractor")
        title.setProperty("class", "ToolTitle")
        desc = QLabel("Deconstruct high-resolution video clips into sequences of high-quality PNG frame assets.")
        desc.setProperty("class", "ToolDesc")
        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        scroll_layout.addLayout(header_layout)
        
        # Drag & Drop Zone
        self.drag_drop = DragDropZone(
            supported_extensions=[".mov", ".mp4", ".mkv", ".avi", ".webm"],
            instruction_text="Drag & drop videos or folders here"
        )
        self.drag_drop.paths_dropped.connect(self.handle_paths_dropped)
        scroll_layout.addWidget(self.drag_drop)
        
        # Assets Manager (Multi-File list)
        self.file_list = SelectedFilesList()
        self.file_list.list_changed.connect(self.update_ui_state)
        scroll_layout.addWidget(self.file_list)
        
        # Destination Preview Card
        dest_card = QFrame()
        dest_card.setProperty("class", "CardFrame")
        dest_layout = QHBoxLayout(dest_card)
        dest_layout.setContentsMargins(15, 12, 15, 12)
        
        dest_lbl = QLabel("Output Destination:")
        dest_lbl.setProperty("class", "FormLabel")
        dest_lbl.setFixedWidth(130)
        self.dest_desc = QLabel("Frames will be extracted to dedicated '[video_name]_frames' folders next to each source video.")
        self.dest_desc.setStyleSheet("color: #8E8E93; font-style: italic;")
        dest_layout.addWidget(dest_lbl)
        dest_layout.addWidget(self.dest_desc, 1)
        scroll_layout.addWidget(dest_card)
        
        # Collapsible Advanced Settings
        self.adv_settings = CollapsibleSection("Advanced Settings")
        
        # Target Output Height
        height_layout = QHBoxLayout()
        height_lbl = QLabel("Target Height (px):")
        height_lbl.setProperty("class", "FormLabel")
        height_lbl.setFixedWidth(160)
        self.height_input = QLineEdit()
        self.height_input.setText("1080")
        self.height_input.setPlaceholderText("e.g., 1080 or 720 or 2160")
        height_layout.addWidget(height_lbl)
        height_layout.addWidget(self.height_input)
        self.adv_settings.add_layout(height_layout)
        
        # PNG Compression Level (0-9)
        png_layout = QHBoxLayout()
        png_lbl = QLabel("PNG Compression Level:")
        png_lbl.setProperty("class", "FormLabel")
        png_lbl.setFixedWidth(160)
        self.png_slider = QSlider(Qt.Horizontal)
        self.png_slider.setRange(0, 9)
        self.png_slider.setValue(3)
        self.png_val_lbl = QLabel("3")
        self.png_val_lbl.setProperty("class", "FormValue")
        self.png_val_lbl.setFixedWidth(30)
        self.png_slider.valueChanged.connect(lambda v: self.png_val_lbl.setText(str(v)))
        png_layout.addWidget(png_lbl)
        png_layout.addWidget(self.png_slider, 1)
        png_layout.addWidget(self.png_val_lbl)
        self.adv_settings.add_layout(png_layout)
        
        # Naming Format Template
        naming_layout = QHBoxLayout()
        naming_lbl = QLabel("Frame Naming Format:")
        naming_lbl.setProperty("class", "FormLabel")
        naming_lbl.setFixedWidth(160)
        self.naming_input = QLineEdit()
        self.naming_input.setText("frame_%06d.png")
        self.naming_input.setPlaceholderText("e.g. frame_%06d.png")
        naming_layout.addWidget(naming_lbl)
        naming_layout.addWidget(self.naming_input)
        self.adv_settings.add_layout(naming_layout)
        
        # Recursive Processing Toggle
        self.recursive_checkbox = QCheckBox("Process directories recursively")
        self.recursive_checkbox.setChecked(False)
        self.adv_settings.add_widget(self.recursive_checkbox)
        
        # Reset Defaults Button
        reset_row = QHBoxLayout()
        reset_row.addStretch()
        self.reset_btn = QPushButton("Reset to Original Defaults")
        self.reset_btn.setProperty("class", "SecondaryBtn")
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.clicked.connect(self.reset_defaults)
        reset_row.addWidget(self.reset_btn)
        self.adv_settings.add_layout(reset_row)
        
        scroll_layout.addWidget(self.adv_settings)
        
        # Output Terminal & Progress Card
        exec_card = QFrame()
        exec_card.setProperty("class", "CardFrame")
        exec_layout = QVBoxLayout(exec_card)
        exec_layout.setSpacing(10)
        
        status_row = QHBoxLayout()
        status_lbl = QLabel("Workflow Status:")
        status_lbl.setProperty("class", "FormLabel")
        self.status_val = QLabel("Idle")
        self.status_val.setProperty("class", "StatusLabel")
        self.status_val.setProperty("status", "idle")
        status_row.addWidget(status_lbl)
        status_row.addWidget(self.status_val)
        status_row.addStretch()
        exec_layout.addLayout(status_row)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        exec_layout.addWidget(self.progress_bar)
        
        self.log_terminal = QTextEdit()
        self.log_terminal.setProperty("class", "LogTerminal")
        self.log_terminal.setReadOnly(True)
        self.log_terminal.setMinimumHeight(150)
        self.log_terminal.setPlaceholderText("Live extraction logs will output here...")
        exec_layout.addWidget(self.log_terminal)
        
        btn_action_row = QHBoxLayout()
        btn_action_row.addStretch()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setProperty("class", "SecondaryBtn")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_workflow)
        btn_action_row.addWidget(self.cancel_btn)
        
        self.run_btn = GlowButton("Run Workflow")
        self.run_btn.setProperty("class", "PrimaryBtn")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self.run_workflow)
        btn_action_row.addWidget(self.run_btn)
        
        exec_layout.addLayout(btn_action_row)
        scroll_layout.addWidget(exec_card)
        
        # 4. Set container on Scroll Area and add to view layout
        scroll_area.setWidget(scroll_container)
        main_layout.addWidget(scroll_area)
        
    def handle_paths_dropped(self, paths):
        valid_paths = []
        invalid_files = []
        video_extensions = {".mov", ".mp4", ".mkv", ".avi", ".webm"}
        
        for p in paths:
            if os.path.isdir(p):
                valid_paths.append(p)
            else:
                ext = os.path.splitext(p)[1].lower()
                if ext in video_extensions:
                    valid_paths.append(p)
                else:
                    invalid_files.append(os.path.basename(p))
                    
        if valid_paths:
            self.file_list.add_paths(valid_paths)
            self.log_terminal.append(f"Added {len(valid_paths)} video assets to queue.")
            
        if invalid_files:
            QMessageBox.warning(
                self,
                "Unsupported Video Formats",
                f"The following video files were rejected (only MOV, MP4, MKV, AVI, and WEBM are supported):\n\n" + 
                "\n".join(invalid_files[:6]) + 
                (f"\n...and {len(invalid_files)-6} more" if len(invalid_files) > 6 else "")
            )
            
    def update_ui_state(self):
        has_files = len(self.file_list.get_paths()) > 0
        self.run_btn.setEnabled(has_files)
        
    def reset_defaults(self):
        self.height_input.setText("1080")
        self.png_slider.setValue(3)
        self.naming_input.setText("frame_%06d.png")
        self.recursive_checkbox.setChecked(False)
        self.log_terminal.append("Settings reset to original hardcoded frame extraction defaults.")
        
    def run_workflow(self):
        paths = self.file_list.get_paths()
        if not paths:
            return
            
        self.run_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.status_val.setText("Running")
        self.status_val.setProperty("status", "running")
        self.status_val.style().polish(self.status_val)
        
        self.log_terminal.clear()
        self.progress_bar.setValue(0)
        
        try:
            height_val = int(self.height_input.text())
        except ValueError:
            height_val = 1080
            self.log_terminal.append("[Invalid Height! Falling back to 1080px]")
            
        self.worker = FrameWorker(
            source_paths=paths,
            target_height=height_val,
            png_compression=self.png_slider.value(),
            frame_naming=self.naming_input.text(),
            recursive=self.recursive_checkbox.isChecked()
        )
        
        self.worker.log_signal.connect(self.log_terminal.append)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.status_signal.connect(self.status_val.setText)
        self.worker.finished_signal.connect(self.workflow_finished)
        
        self.worker.start()
        
    def cancel_workflow(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.log_terminal.append("\n[Workflow Cancelled by User]")
            self.workflow_finished(False, "Cancelled")
            
    def workflow_finished(self, success, message):
        self.run_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        
        if success:
            self.status_val.setText("Success")
            self.status_val.setProperty("status", "success")
            self.parse_and_report_stats()
        else:
            self.status_val.setText("Failed")
            self.status_val.setProperty("status", "error")
            
        self.status_val.style().polish(self.status_val)
        self.progress_bar.setValue(100 if success else 0)
        
    def parse_and_report_stats(self):
        text = self.log_terminal.toPlainText()
        import re
        matches = re.findall(r"Saved (\d+) frames to folder", text)
        if matches:
            total_frames = sum([int(m) for m in matches])
            self.stats_updated.emit(total_frames, 0.0)

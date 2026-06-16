import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QProgressBar, QTextEdit, QSlider, QCheckBox, QMessageBox, QScrollArea
from PySide6.QtCore import Qt, Signal
from ui.components import DragDropZone, CollapsibleSection, SelectedFilesList, GlowButton
from workers.webp_worker import WebPWorker

class ImageToolView(QWidget):
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
        title = QLabel("Image → WebP Optimized")
        title.setProperty("class", "ToolTitle")
        desc = QLabel("Convert PNG and JPG files into highly optimized WebP images with absolute quality tuning.")
        desc.setProperty("class", "ToolDesc")
        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        scroll_layout.addLayout(header_layout)
        
        # Drag & Drop Zone
        self.drag_drop = DragDropZone(
            supported_extensions=[".png", ".jpg", ".jpeg"],
            instruction_text="Drag & drop images or folders here"
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
        self.dest_desc = QLabel("Outputs will be written to 'optimized_webp_output' folders alongside each source asset.")
        self.dest_desc.setStyleSheet("color: #8E8E93; font-style: italic;")
        dest_layout.addWidget(dest_lbl)
        dest_layout.addWidget(self.dest_desc, 1)
        scroll_layout.addWidget(dest_card)
        
        # Collapsible Advanced Settings
        self.adv_settings = CollapsibleSection("Advanced Settings")
        
        # Quality Slider
        q_layout = QHBoxLayout()
        q_lbl = QLabel("WebP Quality:")
        q_lbl.setProperty("class", "FormLabel")
        q_lbl.setFixedWidth(140)
        self.q_slider = QSlider(Qt.Horizontal)
        self.q_slider.setRange(1, 100)
        self.q_slider.setValue(75)
        self.q_val_lbl = QLabel("75%")
        self.q_val_lbl.setProperty("class", "FormValue")
        self.q_val_lbl.setFixedWidth(40)
        self.q_slider.valueChanged.connect(lambda v: self.q_val_lbl.setText(f"{v}%"))
        q_layout.addWidget(q_lbl)
        q_layout.addWidget(self.q_slider, 1)
        q_layout.addWidget(self.q_val_lbl)
        self.adv_settings.add_layout(q_layout)
        
        # Method Slider
        m_layout = QHBoxLayout()
        m_lbl = QLabel("Compression Method:")
        m_lbl.setProperty("class", "FormLabel")
        m_lbl.setFixedWidth(140)
        self.m_slider = QSlider(Qt.Horizontal)
        self.m_slider.setRange(0, 6)
        self.m_slider.setValue(6)
        self.m_val_lbl = QLabel("6 (Slowest)")
        self.m_val_lbl.setProperty("class", "FormValue")
        self.m_val_lbl.setFixedWidth(80)
        self.m_slider.valueChanged.connect(self.update_method_label)
        m_layout.addWidget(m_lbl)
        m_layout.addWidget(self.m_slider, 1)
        m_layout.addWidget(self.m_val_lbl)
        self.adv_settings.add_layout(m_layout)
        
        # Lossless Toggle
        self.lossless_checkbox = QCheckBox("Lossless Compression (exact pixel preservation)")
        self.lossless_checkbox.setChecked(False)
        self.adv_settings.add_widget(self.lossless_checkbox)
        
        # Recursive Processing
        self.recursive_checkbox = QCheckBox("Process subfolders recursively")
        self.recursive_checkbox.setChecked(False)
        self.adv_settings.add_widget(self.recursive_checkbox)
        
        # Reset Defaults
        reset_row = QHBoxLayout()
        reset_row.addStretch()
        self.reset_btn = QPushButton("Reset to Original Defaults")
        self.reset_btn.setProperty("class", "SecondaryBtn")
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.clicked.connect(self.reset_defaults)
        reset_row.addWidget(self.reset_btn)
        self.adv_settings.add_layout(reset_row)
        
        scroll_layout.addWidget(self.adv_settings)
        
        # Output Log & Progress Card
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
        self.log_terminal.setPlaceholderText("Live activity logs will output here...")
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
        image_extensions = {".png", ".jpg", ".jpeg"}
        
        for p in paths:
            if os.path.isdir(p):
                valid_paths.append(p)
            else:
                ext = os.path.splitext(p)[1].lower()
                if ext in image_extensions:
                    valid_paths.append(p)
                else:
                    invalid_files.append(os.path.basename(p))
                    
        if valid_paths:
            self.file_list.add_paths(valid_paths)
            self.log_terminal.append(f"Added {len(valid_paths)} assets to queue.")
            
        if invalid_files:
            QMessageBox.warning(
                self,
                "Unsupported File Formats",
                f"The following files were rejected (only PNG, JPG, and JPEG are supported):\n\n" + 
                "\n".join(invalid_files[:6]) + 
                (f"\n...and {len(invalid_files)-6} more" if len(invalid_files) > 6 else "")
            )
            
    def update_ui_state(self):
        has_files = len(self.file_list.get_paths()) > 0
        self.run_btn.setEnabled(has_files)
        
    def update_method_label(self, val):
        labels = {
            0: "0 (Fastest)",
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6 (Slowest/Max)"
        }
        self.m_val_lbl.setText(labels.get(val, str(val)))
        
    def reset_defaults(self):
        self.q_slider.setValue(75)
        self.m_slider.setValue(6)
        self.lossless_checkbox.setChecked(False)
        self.recursive_checkbox.setChecked(False)
        self.log_terminal.append("Settings reset to original hardcoded workflow defaults.")
        
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
        
        self.worker = WebPWorker(
            source_paths=paths,
            quality=self.q_slider.value(),
            lossless=self.lossless_checkbox.isChecked(),
            method=self.m_slider.value(),
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
        matches = re.findall(r"Size Reduced:\s*([\d\.]+)KB to ([\d\.]+)KB", text)
        if matches:
            count = len(matches)
            total_saved_kb = 0.0
            for orig, new in matches:
                total_saved_kb += (float(orig) - float(new))
            mb_saved = total_saved_kb / 1024.0
            self.stats_updated.emit(count, mb_saved)

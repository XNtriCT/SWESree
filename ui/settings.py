import os
import shutil
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QMessageBox, QFileDialog, QScrollArea
from PySide6.QtCore import Qt, Signal, QSettings

class SettingsView(QWidget):
    stats_cleared = Signal()
    ffmpeg_configured = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("SWESree", "Workflows")
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(25)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        title = QLabel("System Settings")
        title.setProperty("class", "ToolTitle")
        desc = QLabel("Configure environment variables, binary dependencies, and manage workflow telemetry.")
        desc.setProperty("class", "ToolDesc")
        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        scroll_layout.addLayout(header_layout)
        
        # FFmpeg Configurations
        ffmpeg_card = QFrame()
        ffmpeg_card.setProperty("class", "CardFrame")
        ffmpeg_layout = QVBoxLayout(ffmpeg_card)
        ffmpeg_layout.setSpacing(12)
        
        ff_title = QLabel("FFmpeg Compression Dependency")
        ff_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #FFFFFF;")
        ffmpeg_layout.addWidget(ff_title)
        
        self.ff_status_lbl = QLabel("Checking FFmpeg presence...")
        self.ff_status_lbl.setStyleSheet("font-size: 12px; font-weight: 500;")
        ffmpeg_layout.addWidget(self.ff_status_lbl)
        
        path_row = QHBoxLayout()
        path_lbl = QLabel("Custom FFmpeg Path:")
        path_lbl.setProperty("class", "FormLabel")
        path_lbl.setFixedWidth(130)
        
        self.path_input = QLineEdit()
        self.path_input.setText(self.settings.value("ffmpeg_path", ""))
        self.path_input.setPlaceholderText("Leave empty to use system environment PATH")
        self.path_input.textChanged.connect(self.save_ffmpeg_path)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setProperty("class", "SecondaryBtn")
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.setMinimumHeight(32)
        browse_btn.clicked.connect(self.browse_ffmpeg)
        
        path_row.addWidget(path_lbl)
        path_row.addWidget(self.path_input, 1)
        path_row.addWidget(browse_btn)
        ffmpeg_layout.addLayout(path_row)
        
        ff_btn_row = QHBoxLayout()
        ff_btn_row.addStretch()
        check_btn = QPushButton("Test & Verify FFmpeg")
        check_btn.setProperty("class", "SecondaryBtn")
        check_btn.setCursor(Qt.PointingHandCursor)
        check_btn.setMinimumHeight(32)
        check_btn.clicked.connect(self.verify_ffmpeg)
        ff_btn_row.addWidget(check_btn)
        ffmpeg_layout.addLayout(ff_btn_row)
        
        scroll_layout.addWidget(ffmpeg_card)
        
        # Telemetry Card
        telemetry_card = QFrame()
        telemetry_card.setProperty("class", "CardFrame")
        telemetry_layout = QVBoxLayout(telemetry_card)
        telemetry_layout.setSpacing(12)
        
        tel_title = QLabel("Application Telemetry & Analytics")
        tel_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #FFFFFF;")
        
        tel_desc = QLabel("Delete accumulated local stats (images processed, videos compressed, space saved) from the dashboard launcher.")
        tel_desc.setStyleSheet("color: #8E8E93; font-size: 12px;")
        tel_desc.setWordWrap(True)
        
        clear_btn = QPushButton("Reset Dashboard Statistics")
        clear_btn.setProperty("class", "SecondaryBtn")
        clear_btn.setStyleSheet("color: #FF453A; border-color: #FF453A;")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setMinimumHeight(32)
        clear_btn.clicked.connect(self.clear_stats)
        
        telemetry_layout.addWidget(tel_title)
        telemetry_layout.addWidget(tel_desc)
        telemetry_layout.addWidget(clear_btn, 0, Qt.AlignLeft)
        
        scroll_layout.addWidget(telemetry_card)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_container)
        main_layout.addWidget(scroll_area)
        
        self.verify_ffmpeg(silent=True)
        
    def browse_ffmpeg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Locate ffmpeg.exe", "", "FFmpeg Binary (ffmpeg.exe);;All Files (*)")
        if file_path:
            self.path_input.setText(file_path)
            
    def save_ffmpeg_path(self, text):
        self.settings.setValue("ffmpeg_path", text.strip())
        self.ffmpeg_configured.emit()
        
    def verify_ffmpeg(self, silent=False):
        custom_path = self.path_input.text().strip()
        cmd = custom_path if custom_path else "ffmpeg"
            
        try:
            res = subprocess.run([cmd, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            if res.returncode == 0:
                self.ff_status_lbl.setText("✓ FFmpeg is available and active on your system path.")
                self.ff_status_lbl.setStyleSheet("color: #30D158; font-weight: 600;")
                if not silent:
                    QMessageBox.information(self, "FFmpeg Found", "Successfully validated FFmpeg pathway! Video compression and frames extraction are fully active.")
            else:
                self.ff_status_lbl.setText("✗ FFmpeg responded but returned a non-zero exit code.")
                self.ff_status_lbl.setStyleSheet("color: #FF453A; font-weight: 600;")
        except FileNotFoundError:
            self.ff_status_lbl.setText("✗ FFmpeg binary was not found. Please install FFmpeg or set custom path.")
            self.ff_status_lbl.setStyleSheet("color: #FF453A; font-weight: 600;")
            if not silent:
                QMessageBox.critical(self, "FFmpeg Not Found", "FFmpeg is required for MOV to WebM video compression.\n\nPlease locate ffmpeg.exe or add FFmpeg to your system Path.")
        except Exception as e:
            self.ff_status_lbl.setText(f"✗ Error checking FFmpeg: {e}")
            self.ff_status_lbl.setStyleSheet("color: #FF453A; font-weight: 600;")
            
    def clear_stats(self):
        btn = QMessageBox.question(
            self, 
            "Reset Statistics?", 
            "Are you sure you want to clear all accumulated counts and savings statistics? This action is irreversible.",
            QMessageBox.Yes | QMessageBox.No
        )
        if btn == QMessageBox.Yes:
            self.settings.setValue("stats_images_count", 0)
            self.settings.setValue("stats_videos_count", 0)
            self.settings.setValue("stats_mb_saved", 0.0)
            self.stats_cleared.emit()
            QMessageBox.information(self, "Reset Complete", "Dashboard statistics have been successfully cleared.")

class AboutView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(25)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        title = QLabel("About SWESree")
        title.setProperty("class", "ToolTitle")
        desc = QLabel("Creative Production Toolkit — Version 1.0.0")
        desc.setProperty("class", "ToolDesc")
        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        scroll_layout.addLayout(header_layout)
        
        # Content Card
        info_card = QFrame()
        info_card.setProperty("class", "CardFrame")
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(15)
        info_layout.setContentsMargins(20, 20, 20, 20)
        
        logo_placeholder = QLabel("SWESree")
        logo_placeholder.setStyleSheet("font-size: 24px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px;")
        info_layout.addWidget(logo_placeholder)
        
        separator = QFrame()
        separator.setProperty("class", "LineSeparator")
        info_layout.addWidget(separator)
        
        about_text = QLabel(
            "SWESree is a premium native Windows wrapper application designed for high-performance creative production workflows.\n\n"
            "By consolidating tuned image encoding and FFmpeg video compression scripts into an elegant, native Qt graphical environment, "
            "SWESree enables rapid, single-click optimizations without sacrificing advanced controls.\n\n"
            "Designed and built for creators who value clean, responsive design, fast performance, and network payload reduction."
        )
        about_text.setStyleSheet("color: #8E8E93; font-size: 13px; line-height: 20px;")
        about_text.setWordWrap(True)
        info_layout.addWidget(about_text)
        
        tech_title = QLabel("System Core Engine Details:")
        tech_title.setStyleSheet("font-size: 12px; font-weight: 600; color: #FFFFFF; margin-top: 10px;")
        info_layout.addWidget(tech_title)
        
        tech_details = QLabel(
            "• GUI Engine: PySide6 (Qt v6) Framework\n"
            "• Video Processor: FFmpeg Custom VP9 Compressor\n"
            "• Image Core: Pillow (PIL) WebP Engine\n"
            "• Frame Processor: OpenCV (cv2) Lanczos4 Scaler"
        )
        tech_details.setStyleSheet("color: #8E8E93; font-size: 12px; line-height: 18px;")
        info_layout.addWidget(tech_details)
        
        copyright_lbl = QLabel("© 2026 SWESree. All rights reserved.")
        copyright_lbl.setStyleSheet("color: #48484A; font-size: 11px;")
        info_layout.addWidget(copyright_lbl)
        
        scroll_layout.addWidget(info_card)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_container)
        main_layout.addWidget(scroll_area)

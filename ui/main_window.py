import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QStackedWidget, QLabel, QButtonGroup
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon

from ui.dashboard import DashboardView
from ui.image_tool import ImageToolView
from ui.webm_tool import WebMToolView
from ui.frames_tool import FramesToolView
from ui.settings import SettingsView, AboutView

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SWESree")
        self.resize(1000, 750)
        self.setMinimumSize(900, 680)
        
        self.settings = QSettings("SWESree", "Workflows")
        
        # Load stats
        self.stats_images = int(self.settings.value("stats_images_count", 0))
        self.stats_videos = int(self.settings.value("stats_videos_count", 0))
        self.stats_mb_saved = float(self.settings.value("stats_mb_saved", 0.0))
        
        self.init_ui()
        self.update_dashboard_stats()
        
    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Left Sidebar Frame
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarFrame")
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)
        
        # Brand Header
        brand_title = QLabel("SWESree")
        brand_title.setObjectName("SidebarTitle")
        brand_subtitle = QLabel("Productivity Suite")
        brand_subtitle.setObjectName("SidebarSubtitle")
        sidebar_layout.addWidget(brand_title)
        sidebar_layout.addWidget(brand_subtitle)
        
        # Navigation Buttons Group
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)
        
        self.btn_dashboard = QPushButton("📊  Dashboard")
        self.btn_dashboard.setCheckable(True)
        self.btn_dashboard.setChecked(True)
        self.btn_dashboard.setProperty("class", "SidebarBtn")
        self.btn_dashboard.setCursor(Qt.PointingHandCursor)
        self.btn_group.addButton(self.btn_dashboard, 0)
        
        self.btn_webp = QPushButton("🖼️  Image → WebP")
        self.btn_webp.setCheckable(True)
        self.btn_webp.setProperty("class", "SidebarBtn")
        self.btn_webp.setCursor(Qt.PointingHandCursor)
        self.btn_group.addButton(self.btn_webp, 1)
        
        self.btn_webm = QPushButton("⚡  Video → WebM")
        self.btn_webm.setCheckable(True)
        self.btn_webm.setProperty("class", "SidebarBtn")
        self.btn_webm.setCursor(Qt.PointingHandCursor)
        self.btn_group.addButton(self.btn_webm, 2)
        
        self.btn_frames = QPushButton("🎞️  Video → Frames")
        self.btn_frames.setCheckable(True)
        self.btn_frames.setProperty("class", "SidebarBtn")
        self.btn_frames.setCursor(Qt.PointingHandCursor)
        self.btn_group.addButton(self.btn_frames, 3)
        
        self.btn_settings = QPushButton("⚙️  Settings")
        self.btn_settings.setCheckable(True)
        self.btn_settings.setProperty("class", "SidebarBtn")
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_group.addButton(self.btn_settings, 4)
        
        self.btn_about = QPushButton("ℹ️  About")
        self.btn_about.setCheckable(True)
        self.btn_about.setProperty("class", "SidebarBtn")
        self.btn_about.setCursor(Qt.PointingHandCursor)
        self.btn_group.addButton(self.btn_about, 5)
        
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_webp)
        sidebar_layout.addWidget(self.btn_webm)
        sidebar_layout.addWidget(self.btn_frames)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addWidget(self.btn_about)
        
        # Add Stretch at bottom of sidebar
        sidebar_layout.addStretch()
        
        # 2. Main Content Frame (Contains Stacked Views)
        self.content_frame = QFrame()
        self.content_frame.setObjectName("ContentFrame")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Instantiate subviews
        self.dashboard_view = DashboardView()
        self.webp_view = ImageToolView()
        self.webm_view = WebMToolView()
        self.frames_view = FramesToolView()
        self.settings_view = SettingsView()
        self.about_view = AboutView()
        
        # Add to stacked widget (indexes match IDs in QButtonGroup)
        self.stacked_widget.addWidget(self.dashboard_view) # Index 0
        self.stacked_widget.addWidget(self.webp_view)      # Index 1
        self.stacked_widget.addWidget(self.webm_view)      # Index 2
        self.stacked_widget.addWidget(self.frames_view)    # Index 3
        self.stacked_widget.addWidget(self.settings_view)  # Index 4
        self.stacked_widget.addWidget(self.about_view)     # Index 5
        
        # Layout arrangement
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_frame, 1)
        
        # Connect navigation triggers
        self.btn_group.idClicked.connect(self.navigate_to_page)
        
        # Dashboard Launcher navigation overrides
        self.dashboard_view.switch_to_tool.connect(self.navigate_from_dashboard)
        
        # Telemetry connections
        self.webp_view.stats_updated.connect(self.add_image_stats)
        self.webm_view.stats_updated.connect(self.add_video_stats)
        self.frames_view.stats_updated.connect(self.add_frames_stats)
        self.settings_view.stats_cleared.connect(self.reset_stats)
        self.settings_view.ffmpeg_configured.connect(self.reload_ffmpeg_settings)
        
    def navigate_to_page(self, page_id):
        self.stacked_widget.setCurrentIndex(page_id)
        
    def navigate_from_dashboard(self, tool_name):
        mapping = {
            "webp": (self.btn_webp, 1),
            "webm": (self.btn_webm, 2),
            "frames": (self.btn_frames, 3)
        }
        if tool_name in mapping:
            btn, index = mapping[tool_name]
            btn.setChecked(True)
            self.stacked_widget.setCurrentIndex(index)
            
    def update_dashboard_stats(self):
        self.dashboard_view.update_stats(self.stats_images, self.stats_videos, self.stats_mb_saved)
        
    def add_image_stats(self, count, mb_saved):
        self.stats_images += count
        self.stats_mb_saved += mb_saved
        self.save_stats()
        self.update_dashboard_stats()
        
    def add_video_stats(self, count, mb_saved):
        self.stats_videos += count
        self.stats_mb_saved += mb_saved
        self.save_stats()
        self.update_dashboard_stats()
        
    def add_frames_stats(self, count, mb_saved):
        # We don't increment videos compressed for extracting frames, but we can log metrics if needed
        self.save_stats()
        self.update_dashboard_stats()
        
    def save_stats(self):
        self.settings.setValue("stats_images_count", self.stats_images)
        self.settings.setValue("stats_videos_count", self.stats_videos)
        self.settings.setValue("stats_mb_saved", self.stats_mb_saved)
        
    def reset_stats(self):
        self.stats_images = 0
        self.stats_videos = 0
        self.stats_mb_saved = 0.0
        self.update_dashboard_stats()
        
    def reload_ffmpeg_settings(self):
        # Any worker running would check QSettings.value("ffmpeg_path") automatically,
        # but we can also trigger overrides here if cached.
        pass

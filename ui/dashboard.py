from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QScrollArea
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

class StatCard(QFrame):
    def __init__(self, value, label, accent_color="#FF4F00", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setProperty("class", "CardFrame")
        self.setMinimumHeight(85)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(5)
        
        self.val_label = QLabel(value)
        self.val_label.setStyleSheet(f"font-size: 24px; font-weight: 700; color: {accent_color};")
        
        self.desc_label = QLabel(label)
        self.desc_label.setStyleSheet("font-size: 10px; color: #8E8E93; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;")
        
        layout.addWidget(self.val_label)
        layout.addWidget(self.desc_label)

class ToolLauncherCard(QFrame):
    clicked = Signal()
    
    def __init__(self, title, description, icon_text, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setProperty("class", "CardFrame")
        self.setMinimumHeight(160)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("font-size: 24px; color: #FF4F00; font-weight: bold;")
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 15px; font-weight: 700; color: #FFFFFF;")
        
        self.desc_label = QLabel(description)
        self.desc_label.setStyleSheet("font-size: 12px; color: #8E8E93;")
        self.desc_label.setWordWrap(True)
        
        self.launch_btn = QPushButton("Open Tool")
        self.launch_btn.setProperty("class", "SecondaryBtn")
        self.launch_btn.setCursor(Qt.PointingHandCursor)
        self.launch_btn.setMinimumHeight(32)
        self.launch_btn.clicked.connect(self.clicked.emit)
        
        layout.addWidget(icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.desc_label)
        layout.addStretch()
        layout.addWidget(self.launch_btn)

class DashboardView(QWidget):
    switch_to_tool = Signal(str)
    
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
        
        # Header Section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        title = QLabel("Creative Production Hub")
        title.setProperty("class", "ToolTitle")
        
        desc = QLabel("Welcome to SWESree. Optimize, compress, and extract production-grade assets in seconds.")
        desc.setProperty("class", "ToolDesc")
        
        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        scroll_layout.addLayout(header_layout)
        
        # Stats Section
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        self.stat_images = StatCard("0", "Images Optimized", "#FF4F00")
        self.stat_videos = StatCard("0", "Videos Compressed", "#FF9F0A")
        self.stat_frames = StatCard("0.0 MB", "Total Bandwidth Saved", "#30D158")
        
        stats_layout.addWidget(self.stat_images)
        stats_layout.addWidget(self.stat_videos)
        stats_layout.addWidget(self.stat_frames)
        scroll_layout.addLayout(stats_layout)
        
        # Launcher Grid Title
        grid_title = QLabel("Available Toolkits")
        grid_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #FFFFFF; margin-top: 10px;")
        scroll_layout.addWidget(grid_title)
        
        # Launcher Cards Section
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        card1 = ToolLauncherCard(
            "Image → WebP Optimized", 
            "Convert PNG/JPG into ultra-compressed WebP format. Select lossy or lossless presets.", 
            "🖼️"
        )
        card1.clicked.connect(lambda: self.switch_to_tool.emit("webp"))
        
        card2 = ToolLauncherCard(
            "Video → WebM Mobile Stream", 
            "Compress MOV/MP4 to ultra-lightweight WebM for seamless background web playback.", 
            "⚡"
        )
        card2.clicked.connect(lambda: self.switch_to_tool.emit("webm"))
        
        card3 = ToolLauncherCard(
            "Video → Frames Extractor", 
            "Extract video sequence frames to high-fidelity, chronological PNG files at specific heights.", 
            "🎞️"
        )
        card3.clicked.connect(lambda: self.switch_to_tool.emit("frames"))
        
        grid_layout.addWidget(card1, 0, 0)
        grid_layout.addWidget(card2, 0, 1)
        grid_layout.addWidget(card3, 0, 2)
        
        scroll_layout.addLayout(grid_layout)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_container)
        main_layout.addWidget(scroll_area)
        
    def update_stats(self, images_count, videos_count, mb_saved):
        self.stat_images.val_label.setText(str(images_count))
        self.stat_videos.val_label.setText(str(videos_count))
        self.stat_frames.val_label.setText(f"{mb_saved:.1f} MB")

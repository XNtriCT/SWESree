# SWESree

A premium native Windows desktop productivity toolkit for web design workflows. SWESree wraps three battle-tested Python scripts into a beautiful, modern graphical interface powered by PySide6 and QML — designed for daily use by web designers.

## Features

### 🖼️ Image → WebP Conversion
Convert PNG, JPG, and JPEG images to optimized WebP format with configurable quality, lossless mode, and compression method.

### ⚡ Video → WebM Conversion
Transcode MOV, MP4, MKV, and AVI videos to lightweight WebM format with full control over scale, FPS, CRF, bitrate, and audio inclusion.

### 🎞️ Video → Frames Extraction
Extract individual frames from video files as PNG sequences with adjustable target height, compression level, and naming patterns.

### 📊 Dashboard
Track your conversion statistics — total images processed, videos converted, and estimated storage saved.

### ⚙️ Settings
Configure FFmpeg path, verify installation, and manage application preferences.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Python 3.13+ |
| UI Framework | PySide6 (Qt 6 for Python) |
| UI Markup | QML with custom controls |
| Image Processing | Pillow (PIL) |
| Video Processing | FFmpeg (via subprocess) |
| Frame Extraction | OpenCV (cv2) |
| Packaging | PyInstaller |

## Project Structure

```
SWESree/
├── main.py                    # Application entry point & backend bridge
├── requirements.txt           # Python dependencies
├── assets/
│   ├── icon.ico               # Application icon
│   └── logo.svg               # Logo asset
├── qml/
│   ├── main.qml               # Root window & navigation
│   ├── DashboardPage.qml      # Statistics dashboard
│   ├── ImageToolPage.qml      # Image → WebP tool page
│   ├── WebmToolPage.qml       # Video → WebM tool page
│   ├── FramesToolPage.qml     # Video → Frames tool page
│   ├── SettingsPage.qml       # Settings page
│   └── CustomControls/
│       ├── CustomSlider.qml   # Styled slider control
│       ├── DropZone.qml       # Drag-and-drop file zone
│       ├── GlowButton.qml     # Animated action button
│       └── QueueList.qml      # File queue list
├── workers/
│   ├── worker_base.py         # Base thread worker class
│   ├── webp_worker.py         # WebP conversion worker
│   ├── webm_worker.py         # WebM conversion worker
│   └── frame_worker.py        # Frame extraction worker
├── workflows/
│   ├── IMGtoWebp.py           # Core image conversion logic
│   ├── MovtoWebM.py           # Core video conversion logic
│   └── VideoToFrames.py       # Core frame extraction logic
└── ui/
    ├── main_window.py         # Legacy UI window definition
    ├── components.py          # Legacy UI components
    ├── dashboard.py           # Legacy dashboard tab
    ├── image_tool.py          # Legacy image tool tab
    ├── webm_tool.py           # Legacy webm tool tab
    ├── frames_tool.py         # Legacy frames tool tab
    ├── settings.py            # Legacy settings tab
    └── styles.qss             # Qt stylesheet
```

## Getting Started

### Prerequisites

- Python 3.13+
- FFmpeg installed and available in PATH (or configured in Settings)

### Installation

```bash
# Clone the repository
git clone https://github.com/XNtriCT/SWESree.git
cd SWESree

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Building Standalone Executable

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build using the spec file
pyinstaller --noconfirm SWESree.spec

# The executable will be at dist/SWESree.exe
```

## License

This project is for personal use.

# SWESree

<p align="center">
  <strong>A premium Windows desktop toolkit for high-performance web asset optimization.</strong><br>
  Seamlessly convert images, compress videos, and extract frames through a beautifully crafted drag-and-drop interface.
</p>

---

## ✨ Overview

**SWESree** is a modern desktop application built to simplify and accelerate the repetitive asset-processing workflows used in professional web design and digital content creation.

Originally developed to unify a collection of highly refined internal Python utilities, SWESree wraps these production-tested workflows inside a polished graphical interface, eliminating the need for command-line interactions while preserving the speed, flexibility, and precision of the original tools.

Designed with creators in mind, SWESree enables users to simply drag and drop files or folders, click a single button, and receive optimized outputs neatly organized alongside the original assets. The application is engineered to stay out of the way, reducing friction between creative work and technical optimization.

---

## 🚀 Core Features

### 🖼️ Image → Optimized WebP Conversion
- Batch conversion of PNG, JPG, and JPEG files into highly optimized WebP assets.
- Intelligent drag-and-drop support for individual files or entire directories.
- Preserves original source files and automatically creates dedicated output folders.
- Uses carefully tuned default compression settings optimized for modern web performance.
- Optional advanced controls allow temporary adjustment of quality and compression parameters.

### 🎥 Video → Lightweight WebM Compression
- Converts MOV and other supported video formats into highly compressed WebM assets.
- Powered by FFmpeg for reliable, production-grade encoding.
- Optimized for web backgrounds, scrolling animations, and lightweight video delivery.
- Supports adjustable encoding parameters while retaining optimized defaults.
- Automatic output management prevents clutter and accidental overwrites.

### 🎞️ Video → Frame Extraction
- Extracts sequential image frames from video files with high-quality scaling.
- Automatically creates organized output folders for each processed video.
- Preserves aspect ratio and naming consistency.
- Ideal for scroll-based web animations, interactive experiences, and creative workflows.
- Optional controls allow adjustment of output resolution and frame settings.

---

## 🎯 Why SWESree?

Modern web projects demand an increasing amount of asset optimization:
- Converting large images into efficient formats.
- Compressing motion assets for smooth browser playback.
- Breaking videos into frame sequences for interactive experiences.
- Organizing outputs without creating unnecessary project clutter.

Most existing solutions require juggling multiple command-line tools, editing scripts manually, or relying on disconnected utilities.

**SWESree brings these workflows together into a single, intuitive desktop experience.**

Its philosophy is simple:

> **Professional creative tools should feel as refined as the work they help create.**

Instead of exposing technical complexity, SWESree allows users to focus on the creative process while the application handles the repetitive optimization work behind the scenes.

---

## 🖱️ Drag, Drop, Process

Using SWESree is intentionally simple:

1. Launch the application.
2. Drag and drop a file or an entire folder into the appropriate workflow panel.
3. Optionally adjust advanced parameters using the integrated controls.
4. Click **Run Workflow**.
5. Retrieve the processed assets from the automatically generated output folder.

No terminal windows.  
No manual file management.  
No repetitive script execution.

---

## ⚙️ Smart Defaults, Advanced Control

One of the core design principles behind SWESree is preserving the carefully tuned behavior of the underlying Python workflows.

The original scripts serve as the **authoritative processing engines**, and their optimized values remain the default operating mode.

The graphical interface exposes optional sliders and controls for parameters such as:
- Compression quality.
- Encoding settings.
- Target resolution.
- Frame extraction options.
- Processing behavior.

However, these controls are entirely optional.

If no adjustments are made, SWESree executes each workflow using the exact values defined in the original Python implementations, ensuring consistency and preserving the results that have already been tested and refined over time.

---

## 📁 Intelligent Output Management

To maintain a clean and organized workspace, SWESree never overwrites original assets.

Every processing task automatically creates a dedicated output folder within the same directory as the source file or folder. This approach keeps projects tidy while making it easy to compare source and optimized versions side by side.

Example output structure:

```text
Project/
│
├── HeroImage.png
├── BackgroundAnimation.mov
├── ProductDemo.mp4
│
├── optimized_webp_output/
│   └── HeroImage.webp
│
├── webm_output/
│   └── BackgroundAnimation.webm
│
└── ProductDemo_frames/
    ├── frame_000001.png
    ├── frame_000002.png
    └── ...
```

---

## 🎨 Design Philosophy

SWESree is not intended to feel like a traditional utility application or generic administrative dashboard.

The interface is designed around the principles of modern creative software:
- Fluid and responsive interactions.
- Large, intuitive drag-and-drop zones.
- Elegant dark-mode visuals.
- Minimal friction between user intent and execution.
- Clear visual hierarchy and thoughtful spacing.
- A workflow-first experience rather than a settings-first experience.

Every aspect of the application is designed to reduce repetitive effort while providing a polished environment for day-to-day creative production tasks.

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3 |
| Desktop Framework | PySide6 (Qt 6) |
| UI Layer | Qt Quick / QML |
| Image Processing | Pillow (PIL) |
| Video Processing | FFmpeg |
| Computer Vision | OpenCV |
| Packaging | PyInstaller |

---

## 📦 Project Structure

```text
SWESree/
│
├── main.py
├── ui/
├── workflows/
├── workers/
├── assets/
├── build/
├── requirements.txt
└── README.md
```

The architecture cleanly separates:
- **User Interface**
- **Workflow Logic**
- **Background Processing**
- **Asset Management**
- **Packaging & Deployment**

This modular design makes the application easier to maintain and extend with future workflows.

---

## 🔮 Roadmap

Planned future improvements include:

- Additional asset optimization workflows.
- Bulk recursive project processing.
- User-defined workflow presets.
- Configurable export profiles.
- Automatic FFmpeg dependency management.
- Integrated update system.
- Plugin architecture for custom processing modules.
- Extended support for modern image and video formats.

---

## 👨‍💻 Built For

SWESree is designed for professionals and enthusiasts who regularly prepare optimized assets for digital experiences, including:

- Web Designers
- Front-End Developers
- Creative Developers
- Motion Designers
- Digital Agencies
- Content Creators
- Interactive Media Studios
- Anyone working with modern web graphics and animation pipelines.

---

## 📜 Philosophy

SWESree began as a collection of personal workflow scripts refined through practical, real-world use. Over time, those utilities evolved into a cohesive desktop application built around one simple objective:

> **Turn repetitive technical workflows into effortless creative actions.**

The goal is not to replace powerful command-line tools, but to make them more accessible, organized, and enjoyable to use through a thoughtfully designed desktop experience.

---

## 📄 License

This project is intended as a personal productivity and creative workflow toolkit. Licensing terms may be updated as the project evolves.

---

<p align="center">
  <strong>SWESree</strong><br>
  <em>Premium Desktop Workflows for Modern Web Asset Creation.</em>
</p>

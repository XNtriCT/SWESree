import os
import sys
import urllib.parse
from PySide6.QtCore import QObject, Signal, Slot, Property, QSettings, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

# Import background workers
from workers.webp_worker import WebPWorker
from workers.webm_worker import WebMWorker
from workers.frame_worker import FrameWorker

def resolve_resource_path(relative_path):
    """
    Resolve resource paths dynamically to support both development execution 
    and PyInstaller single-file bundle execution.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)

class BackendBridge(QObject):
    # Core system signals
    logReceived = Signal(str, str) # toolName, message
    statsChanged = Signal()
    ffmpegChanged = Signal()
    
    # Progress and Status notification signals
    webpProgressChanged = Signal()
    webpStatusChanged = Signal()
    webmProgressChanged = Signal()
    webmStatusChanged = Signal()
    framesProgressChanged = Signal()
    framesStatusChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("SWESree", "Workflows")
        
        # Load telemetry statistics
        self._stats_images = int(self.settings.value("stats_images_count", 0))
        self._stats_videos = int(self.settings.value("stats_videos_count", 0))
        self._stats_mb_saved = float(self.settings.value("stats_mb_saved", 0.0))
        
        # Load custom FFmpeg path
        self._custom_ffmpeg_path = self.settings.value("ffmpeg_path", "")
        self._ffmpeg_status = "Checking FFmpeg pathway..."
        
        # Internal running states
        self._webp_progress = 0
        self._webp_status = "idle"
        self._webm_progress = 0
        self._webm_status = "idle"
        self._frames_progress = 0
        self._frames_status = "idle"
        
        self.webp_worker = None
        self.webm_worker = None
        self.frames_worker = None
        
        self.verify_ffmpeg_internal()

    # --- Telemetry Properties ---
    @Property(int, notify=statsChanged)
    def statsImages(self):
        return self._stats_images
        
    @Property(int, notify=statsChanged)
    def statsVideos(self):
        return self._stats_videos
        
    @Property(float, notify=statsChanged)
    def statsMbSaved(self):
        return self._stats_mb_saved

    # --- FFmpeg Properties ---
    @Property(str, notify=ffmpegChanged)
    def ffmpegStatus(self):
        return self._ffmpeg_status
        
    @Property(str, notify=ffmpegChanged)
    def customFfmpegPath(self):
        return self._custom_ffmpeg_path

    @Property(QUrl, constant=True)
    def documentsFolder(self):
        from PySide6.QtCore import QStandardPaths
        path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        return QUrl.fromLocalFile(path)

    # --- WebP Properties ---
    @Property(int, notify=webpProgressChanged)
    def webpProgress(self):
        return self._webp_progress
        
    @Property(str, notify=webpStatusChanged)
    def webpStatus(self):
        return self._webp_status

    # --- WebM Properties ---
    @Property(int, notify=webmProgressChanged)
    def webmProgress(self):
        return self._webm_progress
        
    @Property(str, notify=webmStatusChanged)
    def webmStatus(self):
        return self._webm_status

    # --- Video Frames Properties ---
    @Property(int, notify=framesProgressChanged)
    def framesProgress(self):
        return self._frames_progress
        
    @Property(str, notify=framesStatusChanged)
    def framesStatus(self):
        return self._frames_status

    # --- Slots & API Actions ---
    @Slot(list, str, result=list)
    def validatePaths(self, paths, tool_type):
        """
        Cleans QML file URL prefixes and decodes spaces,
        filtering assets by supported formats.
        """
        cleaned = []
        extensions = {
            "webp": {".png", ".jpg", ".jpeg"},
            "webm": {".mov", ".mp4", ".mkv", ".avi", ".webm"},
            "frames": {".mov", ".mp4", ".mkv", ".avi", ".webm"}
        }.get(tool_type, set())
        
        for p in paths:
            path_str = str(p)
            url = QUrl(path_str)
            if url.isValid() and url.isLocalFile():
                path_str = url.toLocalFile()
            else:
                # Safe fallback parsing
                if path_str.startswith("file:///"):
                    path_str = urllib.parse.unquote(path_str[8:])
                elif path_str.startswith("file:"):
                    path_str = urllib.parse.unquote(path_str[5:])
                    
            path_str = os.path.abspath(path_str)
            
            if os.path.exists(path_str):
                if os.path.isdir(path_str):
                    cleaned.append(path_str)
                else:
                    ext = os.path.splitext(path_str)[1].lower()
                    if not extensions or ext in extensions:
                        cleaned.append(path_str)
        return cleaned

    @Slot(str)
    def saveFfmpegPath(self, path):
        cleaned_list = self.validatePaths([path], "frames")
        cleaned_path = cleaned_list[0] if cleaned_list else path
        
        self._custom_ffmpeg_path = cleaned_path.strip()
        self.settings.setValue("ffmpeg_path", self._custom_ffmpeg_path)
        self.ffmpegChanged.emit()
        self.verify_ffmpeg_internal()

    @Slot(bool)
    def verifyFfmpeg(self, silent=True):
        self.verify_ffmpeg_internal(silent)

    def verify_ffmpeg_internal(self, silent=True):
        import subprocess
        cmd = self._custom_ffmpeg_path if self._custom_ffmpeg_path else "ffmpeg"
        try:
            res = subprocess.run([cmd, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            if res.returncode == 0:
                self._ffmpeg_status = "✓ FFmpeg is available and active on your system path."
            else:
                self._ffmpeg_status = "✗ FFmpeg responded but returned an error code."
        except Exception:
            self._ffmpeg_status = "✗ FFmpeg binary was not found. Please locate it or add it to system PATH."
        self.ffmpegChanged.emit()

    @Slot()
    def resetStats(self):
        self._stats_images = 0
        self._stats_videos = 0
        self._stats_mb_saved = 0.0
        self.settings.setValue("stats_images_count", 0)
        self.settings.setValue("stats_videos_count", 0)
        self.settings.setValue("stats_mb_saved", 0.0)
        self.statsChanged.emit()

    # --- WebP Workflow Management ---
    @Slot(list, int, bool, int, bool)
    def startWebpWorkflow(self, paths, quality, lossless, method, recursive):
        if self._webp_status == "running":
            return
            
        self._webp_status = "running"
        self._webp_progress = 0
        self.webpStatusChanged.emit()
        self.webpProgressChanged.emit()
        
        self.webp_worker = WebPWorker(
            source_paths=self.validatePaths(paths, "webp"),
            quality=quality,
            lossless=lossless,
            method=method,
            recursive=recursive
        )
        
        self.webp_worker.log_signal.connect(lambda msg: self.logReceived.emit("webp", msg))
        self.webp_worker.progress_signal.connect(self.update_webp_progress)
        self.webp_worker.finished_signal.connect(self.webp_finished)
        self.webp_worker.start()
        
    def update_webp_progress(self, val):
        self._webp_progress = val
        self.webpProgressChanged.emit()
        
    def webp_finished(self, success, msg):
        self._webp_status = "success" if success else "error"
        self._webp_progress = 100 if success else 0
        self.webpStatusChanged.emit()
        self.webpProgressChanged.emit()
        self.logReceived.emit("webp", f"\n[Process Finished: {msg}]")
        
        if success:
            count = len(self.webp_worker.source_paths)
            self._stats_images += count
            self._stats_mb_saved += count * 0.15 # Estimate 150KB saved per image
            self.settings.setValue("stats_images_count", self._stats_images)
            self.settings.setValue("stats_mb_saved", self._stats_mb_saved)
            self.statsChanged.emit()

    @Slot()
    def cancelWebpWorkflow(self):
        if self.webp_worker and self.webp_worker.isRunning():
            self.webp_worker.stop()
            self.webp_worker.wait()
            self.webp_finished(False, "Cancelled by user.")

    # --- WebM Workflow Management ---
    @Slot(list, str, str, int, str, str, bool)
    def startWebmWorkflow(self, paths, scale, fps, crf, bitrate, g, include_audio):
        if self._webm_status == "running":
            return
            
        self._webm_status = "running"
        self._webm_progress = 0
        self.webmStatusChanged.emit()
        self.webmProgressChanged.emit()
        
        self.webm_worker = WebMWorker(
            source_paths=self.validatePaths(paths, "webm"),
            scale=scale,
            fps=fps,
            crf=crf,
            bitrate=bitrate,
            g=g,
            include_audio=include_audio
        )
        
        self.webm_worker.log_signal.connect(lambda msg: self.logReceived.emit("webm", msg))
        self.webm_worker.progress_signal.connect(self.update_webm_progress)
        self.webm_worker.finished_signal.connect(self.webm_finished)
        self.webm_worker.start()
        
    def update_webm_progress(self, val):
        self._webm_progress = val
        self.webmProgressChanged.emit()
        
    def webm_finished(self, success, msg):
        self._webm_status = "success" if success else "error"
        self._webm_progress = 100 if success else 0
        self.webmStatusChanged.emit()
        self.webmProgressChanged.emit()
        self.logReceived.emit("webm", f"\n[Process Finished: {msg}]")
        
        if success:
            count = len(self.webm_worker.source_paths)
            self._stats_videos += count
            self._stats_mb_saved += count * 4.2 # Estimate 4.2MB saved per video
            self.settings.setValue("stats_videos_count", self._stats_videos)
            self.settings.setValue("stats_mb_saved", self._stats_mb_saved)
            self.statsChanged.emit()

    @Slot()
    def cancelWebmWorkflow(self):
        if self.webm_worker and self.webm_worker.isRunning():
            self.webm_worker.stop()
            self.webm_worker.wait()
            self.webm_finished(False, "Cancelled by user.")

    # --- Frames Workflow Management ---
    @Slot(list, int, int, str, bool)
    def startFramesWorkflow(self, paths, target_height, png_compression, frame_naming, recursive):
        if self._frames_status == "running":
            return
            
        self._frames_status = "running"
        self._frames_progress = 0
        self.framesStatusChanged.emit()
        self.framesProgressChanged.emit()
        
        self.frames_worker = FrameWorker(
            source_paths=self.validatePaths(paths, "frames"),
            target_height=target_height,
            png_compression=png_compression,
            frame_naming=frame_naming,
            recursive=recursive
        )
        
        self.frames_worker.log_signal.connect(lambda msg: self.logReceived.emit("frames", msg))
        self.frames_worker.progress_signal.connect(self.update_frames_progress)
        self.frames_worker.finished_signal.connect(self.frames_finished)
        self.frames_worker.start()
        
    def update_frames_progress(self, val):
        self._frames_progress = val
        self.framesProgressChanged.emit()
        
    def frames_finished(self, success, msg):
        self._frames_status = "success" if success else "error"
        self._frames_progress = 100 if success else 0
        self.framesStatusChanged.emit()
        self.framesProgressChanged.emit()
        self.logReceived.emit("frames", f"\n[Process Finished: {msg}]")

    @Slot()
    def cancelFramesWorkflow(self):
        if self.frames_worker and self.frames_worker.isRunning():
            self.frames_worker.stop()
            self.frames_worker.wait()
            self.frames_finished(False, "Cancelled by user.")

# Native WndProc subclassing for Windows borderless window management (Aero Snap + Shadows)
if os.name == "nt":
    import ctypes
    from ctypes import wintypes
    
    # Types and Constants
    WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_int64, wintypes.HWND, ctypes.c_uint, ctypes.c_size_t, ctypes.c_size_t)
    GWLP_WNDPROC = -4
    
    class RECT(ctypes.Structure):
        _fields_ = [
            ('left', ctypes.c_long),
            ('top', ctypes.c_long),
            ('right', ctypes.c_long),
            ('bottom', ctypes.c_long)
        ]
        
    class NCCALCSIZE_PARAMS(ctypes.Structure):
        _fields_ = [
            ('rgrc', RECT * 3),
            ('lppos', ctypes.c_void_p)
        ]
        
    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', ctypes.c_ulong),
            ('rcMonitor', RECT),
            ('rcWork', RECT),
            ('dwFlags', ctypes.c_ulong)
        ]
        
    # Configure CallWindowProcW argtypes/restype properly to handle 64-bit pointers
    ctypes.windll.user32.CallWindowProcW.restype = ctypes.c_int64
    ctypes.windll.user32.CallWindowProcW.argtypes = [ctypes.c_void_p, wintypes.HWND, ctypes.c_uint, ctypes.c_size_t, ctypes.c_size_t]
    
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        ctypes.windll.user32.GetWindowLongPtrW.restype = ctypes.c_void_p
        ctypes.windll.user32.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
        ctypes.windll.user32.SetWindowLongPtrW.restype = ctypes.c_void_p
        ctypes.windll.user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p]
    else:
        ctypes.windll.user32.GetWindowLongW.restype = ctypes.c_void_p
        ctypes.windll.user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
        ctypes.windll.user32.SetWindowLongW.restype = ctypes.c_void_p
        ctypes.windll.user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p]

def main():
    # GPU acceleration configurations for QML
    os.environ["QSG_RENDER_LOOP"] = "basic"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QGuiApplication(sys.argv)
    
    # Load QML Engine
    engine = QQmlApplicationEngine()
    
    # Instantiate Backend bridge and register QML context property
    backend = BackendBridge()
    engine.rootContext().setContextProperty("backend", backend)
    
    qml_file = resolve_resource_path("qml/main.qml")
    engine.load(QUrl.fromLocalFile(qml_file))
    
    if not engine.rootObjects():
        sys.exit(-1)
        
    root_window = engine.rootObjects()[0]
    if os.name == "nt":
        hwnd = int(root_window.winId())
        
        # Ensure native style has WS_THICKFRAME and WS_CAPTION to allow Aero Snap and shadows
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16) # GWL_STYLE
        # WS_THICKFRAME (0x00040000), WS_CAPTION (0x00C00000), WS_MAXIMIZEBOX (0x00010000), WS_MINIMIZEBOX (0x00020000)
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style | 0x00040000 | 0x00C00000 | 0x00010000 | 0x00020000)
        
        old_wndproc = None
        
        def wndproc(hwnd_val, msg, wparam, lparam):
            if msg == 0x0083: # WM_NCCALCSIZE
                if wparam:
                    try:
                        if ctypes.windll.user32.IsZoomed(hwnd_val):
                            hmonitor = ctypes.windll.user32.MonitorFromWindow(hwnd_val, 2) # MONITOR_DEFAULTTONEAREST
                            monitor_info = MONITORINFO()
                            monitor_info.cbSize = ctypes.sizeof(MONITORINFO)
                            if ctypes.windll.user32.GetMonitorInfoW(hmonitor, ctypes.byref(monitor_info)):
                                params = ctypes.cast(lparam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents
                                params.rgrc[0] = monitor_info.rcWork
                    except Exception:
                        pass
                    return 0
                    
            elif msg == 0x0084: # WM_NCHITTEST
                x = ctypes.c_short(lparam & 0xFFFF).value
                y = ctypes.c_short((lparam >> 16) & 0xFFFF).value
                
                rect = wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd_val, ctypes.byref(rect))
                
                client_x = x - rect.left
                client_y = y - rect.top
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                
                border_width = 8
                
                # Resizing borders (only when not maximized)
                if not ctypes.windll.user32.IsZoomed(hwnd_val):
                    if client_y < border_width:
                        if client_x < border_width:
                            return 13 # HTTOPLEFT
                        elif client_x > width - border_width:
                            return 14 # HTTOPRIGHT
                        else:
                            return 12 # HTTOP
                    elif client_y > height - border_width:
                        if client_x < border_width:
                            return 16 # HTBOTTOMLEFT
                        elif client_x > width - border_width:
                            return 17 # HTBOTTOMRIGHT
                        else:
                            return 15 # HTBOTTOM
                    elif client_x < border_width:
                        return 10 # HTLEFT
                    elif client_x > width - border_width:
                        return 11 # HTRIGHT
                
                # Custom titlebar dragging/double-click
                # Titlebar is 40px height. Exclude the buttons on the right (width - 120px)
                titlebar_min_y = 0 if ctypes.windll.user32.IsZoomed(hwnd_val) else border_width
                if titlebar_min_y <= client_y <= 40:
                    if client_x < (width - 120):
                        return 2 # HTCAPTION
                        
            return ctypes.windll.user32.CallWindowProcW(old_wndproc, hwnd_val, msg, wparam, lparam)
            
        # Bind the callback to the app structure to prevent garbage collection
        global app_wndproc_callback
        app_wndproc_callback = WNDPROC(wndproc)
        
        if ctypes.sizeof(ctypes.c_void_p) == 8:
            old_wndproc = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWLP_WNDPROC)
            ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWLP_WNDPROC, app_wndproc_callback)
        else:
            old_wndproc = ctypes.windll.user32.GetWindowLongW(hwnd, GWLP_WNDPROC)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWLP_WNDPROC, app_wndproc_callback)
            
        # Trigger frame recalculation
        ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027) # SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

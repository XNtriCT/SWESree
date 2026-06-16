from workers.worker_base import BaseWorker
from workflows.VideoToFrames import extract_frames_to_1080p

class FrameWorker(BaseWorker):
    def __init__(self, source_paths, target_height=1080, png_compression=3, frame_naming="frame_%06d.png", recursive=False, parent=None):
        super().__init__(parent)
        self.source_paths = source_paths
        self.target_height = target_height
        self.png_compression = png_compression
        self.frame_naming = frame_naming
        self.recursive = recursive

    def run(self):
        try:
            self.status_signal.emit("Extracting frames...")
            self.progress_signal.emit(0)
            
            extract_frames_to_1080p(
                source_paths=self.source_paths,
                target_height=self.target_height,
                png_compression=self.png_compression,
                frame_naming=self.frame_naming,
                recursive=self.recursive,
                callback=self.handle_callback
            )
            
            if self.is_running:
                self.finished_signal.emit(True, "Video frames extraction complete.")
            else:
                self.finished_signal.emit(False, "Workflow cancelled.")
        except Exception as e:
            self.log_signal.emit(f"Worker Exception: {e}")
            self.finished_signal.emit(False, f"Failed: {e}")

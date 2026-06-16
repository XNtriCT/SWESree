from workers.worker_base import BaseWorker
from workflows.IMGtoWebp import batch_convert_to_optimized_webp

class WebPWorker(BaseWorker):
    def __init__(self, source_paths, quality=75, lossless=False, method=6, recursive=False, parent=None):
        super().__init__(parent)
        self.source_paths = source_paths
        self.quality = quality
        self.lossless = lossless
        self.method = method
        self.recursive = recursive

    def run(self):
        try:
            self.status_signal.emit("Optimizing image assets...")
            self.progress_signal.emit(0)
            
            batch_convert_to_optimized_webp(
                source_paths=self.source_paths,
                quality=self.quality,
                lossless=self.lossless,
                method=self.method,
                recursive=self.recursive,
                callback=self.handle_callback
            )
            
            if self.is_running:
                self.finished_signal.emit(True, "WebP optimization complete.")
            else:
                self.finished_signal.emit(False, "Workflow cancelled.")
        except Exception as e:
            self.log_signal.emit(f"Worker Exception: {e}")
            self.finished_signal.emit(False, f"Failed: {e}")

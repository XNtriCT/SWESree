import os
from pathlib import Path
from workers.worker_base import BaseWorker
from workflows.MovtoWebM import extreme_mobile_webm_compressor

class WebMWorker(BaseWorker):
    def __init__(self, source_paths, scale="1280:-2", fps="20", crf="36", bitrate="800k", g="1", include_audio=False, parent=None):
        super().__init__(parent)
        self.source_paths = source_paths
        self.scale = scale
        self.fps = fps
        self.crf = crf
        self.bitrate = bitrate
        self.g = g
        self.include_audio = include_audio

    def run(self):
        try:
            self.status_signal.emit("Analyzing video assets...")
            self.progress_signal.emit(0)

            video_extensions = {".mov", ".mp4", ".mkv", ".avi", ".webm"}
            files_to_compress = []

            for p in self.source_paths:
                path_obj = Path(p)
                if path_obj.is_file():
                    if path_obj.suffix.lower() in video_extensions:
                        files_to_compress.append(path_obj)
                elif path_obj.is_dir():
                    for f in path_obj.iterdir():
                        if f.is_file() and f.suffix.lower() in video_extensions:
                            files_to_compress.append(f)

            # De-duplicate files while preserving order
            seen = set()
            files_to_compress = [x for x in files_to_compress if not (x in seen or seen.add(x))]

            if not files_to_compress:
                self.log_signal.emit("No valid video files found to compress.")
                self.finished_signal.emit(False, "No video assets found.")
                return

            total_files = len(files_to_compress)
            self.log_signal.emit(f"Found {total_files} video assets to compress.")

            for index, file_path in enumerate(files_to_compress):
                if not self.is_running:
                    break

                folder_path = str(file_path.parent)
                input_name = file_path.name
                output_dir_name = "optimized_webm_output"
                output_name = f"{output_dir_name}/{file_path.stem}.webm"
                
                self.log_signal.emit(f"\nCompressing ({index + 1}/{total_files}): {input_name}")
                
                def file_callback(status, message, progress_percentage=None):
                    if not self.is_running:
                        return
                    if status == "log":
                        self.log_signal.emit(message)
                    elif status == "progress" and progress_percentage is not None:
                        aggregate_pct = int(((index * 100) + progress_percentage) / total_files)
                        self.progress_signal.emit(aggregate_pct)
                        self.status_signal.emit(f"Asset {index+1}/{total_files} — Compressing... {progress_percentage}%")
                    elif status == "error":
                        self.log_signal.emit(f"Error: {message}")
                    elif status == "success":
                        self.log_signal.emit(message)

                extreme_mobile_webm_compressor(
                    folder_path=folder_path,
                    input_name=input_name,
                    output_name=output_name,
                    scale=self.scale,
                    fps=self.fps,
                    crf=self.crf,
                    bitrate=self.bitrate,
                    g=self.g,
                    include_audio=self.include_audio,
                    callback=file_callback
                )
                
                progress_pct = int(((index + 1) / total_files) * 100)
                self.progress_signal.emit(progress_pct)
                self.status_signal.emit(f"Completed {index + 1}/{total_files} videos")

            if self.is_running:
                self.finished_signal.emit(True, f"WebM compression complete. Compressed {total_files} videos.")
            else:
                self.finished_signal.emit(False, "Workflow cancelled.")
        except Exception as e:
            self.log_signal.emit(f"Worker Exception: {e}")
            self.finished_signal.emit(False, f"Failed: {e}")

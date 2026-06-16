from PySide6.QtCore import QThread, Signal

class BaseWorker(QThread):
    log_signal = Signal(str)            # Standard activity log
    progress_signal = Signal(int)       # Progress bar percentage (0-100)
    status_signal = Signal(str)         # Subtitle or running status text
    finished_signal = Signal(bool, str) # Emitted on completion (success: bool, msg: str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_running = True

    def stop(self):
        self.is_running = False

    def handle_callback(self, status, message, progress_percentage=None):
        if not self.is_running:
            return
            
        if status == "log":
            self.log_signal.emit(message)
        elif status == "progress":
            # Strip extra spaces and frame progress logs to look neat
            clean_msg = message.strip()
            if clean_msg:
                self.status_signal.emit(clean_msg)
            if progress_percentage is not None:
                self.progress_signal.emit(progress_percentage)
        elif status == "success":
            self.log_signal.emit(message)
            self.status_signal.emit("Success")
            if progress_percentage is not None:
                self.progress_signal.emit(progress_percentage)
        elif status == "error":
            self.log_signal.emit(f"Error: {message}")
            self.status_signal.emit("Failed")
            if progress_percentage is not None:
                self.progress_signal.emit(progress_percentage)

import subprocess
from pathlib import Path
import re

def extreme_mobile_webm_compressor(folder_path: str, input_name: str, output_name: str,
                                   scale="1280:-2", fps="20", crf="36", bitrate="800k", g="1", include_audio=False, callback=None):
    """
    Converts a MOV video into an ultra-lightweight WebM file specifically 
    engineered to load instantly on 3G/4G networks while preserving fluid scrolling.
    """
    def log(message, status="log", progress_percentage=None):
        print(message)
        if callback:
            callback(status, message, progress_percentage)

    directory = Path(folder_path)
    source = directory / input_name
    destination = directory / output_name

    if not source.exists():
        log(f"Error: Could not locate '{input_name}' in the directory.", "error")
        return

    # Ensure output parent directory exists
    destination.parent.mkdir(exist_ok=True, parents=True)

    # Build command based on overrides or defaults
    command = ["ffmpeg", "-y", "-i", str(source)]
    
    if scale:
        command.extend(["-vf", f"scale={scale}"])
    if fps:
        command.extend(["-r", str(fps)])
        
    command.extend(["-c:v", "libvpx-vp9"])
    
    if crf:
        command.extend(["-crf", str(crf)])
    if bitrate:
        command.extend(["-b:v", str(bitrate)])
    if g:
        command.extend(["-g", str(g)])
        
    command.extend(["-pix_fmt", "yuv420p"])
    
    if include_audio:
        # standard webm audio codec is opus
        command.extend(["-c:a", "libopus"])
    else:
        command.append("-an")
        
    command.append(str(destination))

    log("Executing maximum compression matrix locally...")
    log(f"Command: {' '.join(command)}")

    try:
        # Run process and capture stdout/stderr together
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
            encoding='utf-8',
            errors='replace'
        )

        duration_secs = 0.0
        # Parse output for progress information
        for line in process.stdout:
            line_str = line.strip()
            log(line_str)
            
            # Find video duration
            if "Duration:" in line_str:
                match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", line_str)
                if match:
                    hours, mins, secs = match.groups()
                    duration_secs = int(hours) * 3600 + int(mins) * 60 + float(secs)
                    log(f"Detected video duration: {duration_secs:.2f} seconds")
            
            # Find current processing time
            if "time=" in line_str and duration_secs > 0:
                match = re.search(r"time=\s*(\d+):(\d+):(\d+\.\d+)", line_str)
                if match:
                    hours, mins, secs = match.groups()
                    current_secs = int(hours) * 3600 + int(mins) * 60 + float(secs)
                    pct = min(100.0, (current_secs / duration_secs) * 100.0)
                    log(f"Compressing... {pct:.1f}%", "progress", progress_percentage=int(pct))

        process.wait()
        if process.returncode == 0:
            log(f"\nSuccess! Extreme optimized mobile asset built at:\n{destination}", "success", progress_percentage=100)
        else:
            log(f"\nError: FFmpeg exited with non-zero code {process.returncode}", "error")
            
    except FileNotFoundError:
        log("\nError: FFmpeg is missing from your computer's system path environment.", "error")
    except Exception as e:
        log(f"\nProcessing issue encountered: {e}", "error")

if __name__ == "__main__":
    # Path to your asset layout workspace
    workspace = r"C:\Users\merin\Documents\My Web Designs\1. AMG Jets\Scrollable Animation"
    
    # ⚠️ Double check that your video filename matches this extension accurately
    video_input = "input_animation.mov" 
    video_output = "amg_bg_scroll_mobile.webm"
    
    extreme_mobile_webm_compressor(workspace, video_input, video_output)

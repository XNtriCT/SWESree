import os
import cv2
from pathlib import Path

def extract_frames_to_1080p(source_paths=None, target_height=1080, png_compression=3, frame_naming="frame_%06d.png", recursive=False, callback=None):
    """
    Extracts frames from video files, scales them to a target height, and saves them as lossless PNG images.
    """
    def log(message, status="log", progress_percentage=None):
        print(message)
        if callback:
            callback(status, message, progress_percentage)

    # Resolve input paths to video file list
    video_files = []
    
    if source_paths is None:
        paths = [os.getcwd()]
    elif isinstance(source_paths, (str, Path)):
        paths = [str(source_paths)]
    else:
        paths = [str(p) for p in source_paths]

    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
    
    for path in paths:
        if os.path.isfile(path):
            if path.lower().endswith(video_extensions):
                video_files.append(path)
        elif os.path.isdir(path):
            if recursive:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if f.lower().endswith(video_extensions):
                            video_files.append(os.path.join(root, f))
            else:
                for f in os.listdir(path):
                    full_p = os.path.join(path, f)
                    if os.path.isfile(full_p) and f.lower().endswith(video_extensions):
                        video_files.append(full_p)

    # De-duplicate files
    seen = set()
    video_files = [x for x in video_files if not (x in seen or seen.add(x))]

    if not video_files:
        log(f"No video files found in: {', '.join(paths)}", "error")
        return

    log(f"Found {len(video_files)} video(s). Starting extraction...\n")

    for index, video_path in enumerate(video_files):
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_dir = os.path.dirname(video_path)
        output_dir = os.path.join(video_dir, f"{video_name}_frames")
        os.makedirs(output_dir, exist_ok=True)
        
        log(f"Processing: '{os.path.basename(video_path)}'...")
        log(f"Output folder: '{output_dir}'")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            log(f"Error: Could not open video file '{os.path.basename(video_path)}'", "error")
            continue
            
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        log(f"Total frames to extract: {total_frames}")
        
        while True:
            success, frame = cap.read()
            if not success:
                break
                
            height, width = frame.shape[:2]
            target_width = int((target_height / max(1, height)) * width)
            
            if height != target_height:
                frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
            
            # Save frame
            if "%" in frame_naming:
                try:
                    frame_filename = os.path.join(output_dir, frame_naming % frame_count)
                except Exception:
                    frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.png")
            elif "{" in frame_naming:
                try:
                    frame_filename = os.path.join(output_dir, frame_naming.format(frame_count=frame_count))
                except Exception:
                    frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.png")
            else:
                frame_filename = os.path.join(output_dir, f"{frame_naming}_{frame_count:06d}.png")
            
            cv2.imwrite(frame_filename, frame, [cv2.IMWRITE_PNG_COMPRESSION, png_compression])
            
            frame_count += 1
            
            if frame_count % 10 == 0 or frame_count == total_frames:
                pct = min(100, int((frame_count / max(1, total_frames)) * 100))
                # Calculate aggregate progress
                overall_pct = int(((index * 100) + pct) / len(video_files))
                log(f"  -> Extracted {frame_count}/{total_frames} frames...", "progress", progress_percentage=overall_pct)
                
        cap.release()
        log(f"\nFinished '{os.path.basename(video_path)}'. Saved {frame_count} frames to folder: '{output_dir}'\n")
        log("-" * 50)

    log("All tasks complete!", "success", progress_percentage=100)

if __name__ == "__main__":
    extract_frames_to_1080p()

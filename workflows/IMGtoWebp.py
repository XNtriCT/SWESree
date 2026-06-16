import os
from pathlib import Path
from PIL import Image

def batch_convert_to_optimized_webp(source_paths=None, output_dir_name="optimized_webp_output", quality=75, lossless=False, method=6, recursive=False, callback=None):
    def log(message, status="log", progress_percentage=None):
        print(message)
        if callback:
            callback(status, message, progress_percentage)

    # Resolve input paths to file list
    files_to_convert = []
    
    if source_paths is None:
        paths = [Path(os.getcwd())]
    elif isinstance(source_paths, (str, Path)):
        paths = [Path(source_paths)]
    else:
        paths = [Path(p) for p in source_paths]

    if not paths:
        log("No input paths provided.", "error")
        return

    # Determine destination folder (parent of first file, or first directory itself)
    first_path = paths[0]
    if first_path.is_file():
        output_dir = first_path.parent / output_dir_name
    else:
        output_dir = first_path / output_dir_name

    valid_extensions = {".png", ".jpg", ".jpeg"}
    
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in valid_extensions:
                files_to_convert.append(path)
        elif path.is_dir():
            if recursive:
                files_to_convert.extend([
                    f for f in path.rglob("*")
                    if f.is_file() and f.suffix.lower() in valid_extensions and output_dir not in f.parents
                ])
            else:
                files_to_convert.extend([
                    f for f in path.iterdir()
                    if f.is_file() and f.suffix.lower() in valid_extensions
                ])

    # De-duplicate files
    seen = set()
    files_to_convert = [x for x in files_to_convert if not (x in seen or seen.add(x))]

    if not files_to_convert:
        log(f"No matching PNG or JPG images found in: {', '.join(str(p) for p in paths)}", "error")
        return

    # Ensure the output directory exists
    output_dir.mkdir(exist_ok=True)
    log(f"Output Directory: {output_dir}")
    log(f"Found {len(files_to_convert)} assets to process.\n" + "-"*40)

    success_count = 0
    total_files = len(files_to_convert)

    for index, file_path in enumerate(files_to_convert):
        try:
            with Image.open(file_path) as img:
                if img.mode in ('RGBA', 'LA') and file_path.suffix.lower() in {'.jpg', '.jpeg'}:
                    background = Image.new('RGBA', img.size, (255, 255, 255))
                    img = Image.alpha_composite(background, img).convert('RGB')
                
                output_file_path = output_dir / f"{file_path.stem}.webp"
                
                img.save(
                    output_file_path,
                    "WEBP",
                    quality=quality,
                    lossless=lossless,
                    method=method
                )
                
                orig_size = file_path.stat().st_size / 1024
                new_size = output_file_path.stat().st_size / 1024
                reduction = ((orig_size - new_size) / max(0.001, orig_size)) * 100
                
                log(f"✓ Optimized: {file_path.name} -> {output_file_path.name}")
                log(f"  Size Reduced: {orig_size:.1f}KB to {new_size:.1f}KB (-{reduction:.1f}%)")
                success_count += 1
                
        except Exception as e:
            log(f"✗ Failed to process {file_path.name}. Error: {e}", "error")
            
        progress_pct = int(((index + 1) / total_files) * 100)
        log(f"Optimizing assets... {progress_pct}%", "progress", progress_percentage=progress_pct)

    log("-"*40 + f"\nProcess Complete. Successfully optimized {success_count} assets.")

if __name__ == "__main__":
    batch_convert_to_optimized_webp()

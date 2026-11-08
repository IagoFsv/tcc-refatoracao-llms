import os
from pathlib import Path

def _get_directories():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    if len(input_dir) == 0 or len(output_dir) == 0:
        raise ValueError("Input and output directories must be specified")
    return Path(input_dir), Path(output_dir)

def _validate_input_directory(input_dir):
    if not input_dir.exists():
        raise ValueError("Input directory does not exist")

def _check_duplicate_files(input_dir, output_dir):
    if output_dir.exists():
        file_names = {x.name for x in output_dir.iterdir()}
        existing_files = {file.name for file in input_dir.iterdir()}
        if existing_files.intersection(file_names):
            overwrite = input("Overwrite files? (y/n): ")
            if overwrite != "y":
                raise ValueError("Exiting")

def _get_conversion_flags():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")
    return {
        "start_time": start_time,
        "duration": duration,
        "crop_params": crop_params,
        "crf": crf
    }

def _parse_conversion_flags(flags):
    start_flag = ("-ss " + flags["start_time"]) if flags["start_time"] else ""
    duration_flag = ("-t " + flags["duration"]) if flags["duration"] else ""
    crop_params = flags["crop_params"]
    crf = flags["crf"]
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params else ""
    compression_filter = "-crf " + str(crf) if crf else ""
    return start_flag, duration_flag, crop_filter, compression_filter

def _create_output_directory(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

def _process_files(input_dir, output_dir, flags):
    pre_flags, post_flags, crop_filter, compression_filter = _parse_conversion_flags(flags)
    preview = input("Generate preview thumbnails? (y/n): ") == "y"
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = _get_directories()
    _validate_input_directory(input_dir)
    _check_duplicate_files(input_dir, output_dir)
    flags = _get_conversion_flags()
    _create_output_directory(output_dir)
    _process_files(input_dir, output_dir, flags)

def executar():
    return main()

if __name__ == "__main__":
    executar()

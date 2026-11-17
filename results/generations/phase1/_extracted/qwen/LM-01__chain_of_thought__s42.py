"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def get_user_input():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None

    return Path(input_dir), Path(output_dir)

def validate_directories(input_dir, output_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False

    return True

def validate_files(input_dir, output_dir):
    file_names = [x.name for x in output_dir.iterdir()]
    for file in input_dir.iterdir():
        if file.name in file_names:
            print("Some files already exist in the output directory")

            # Ask user if they want to overwrite files
            overwrite = input("Overwrite files? (y/n): ")
            if overwrite != "y":
                print("Exiting")
                input("Press enter to exit")
                return False

    return True

def get_processing_flags(start_time, duration, crop_params, crf):
    pre_flags = ("-ss " + start_time) if start_time is not None else ""
    duration_flag = ("-t " + duration) if duration is not None else ""

    if crop_params is not None:
        crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params)
    else:
        crop_filter = ""

    if crf is not None:
        compression_filter = "-crf " + str(crf)
    else:
        compression_filter = ""

    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    return pre_flags, post_flags.strip()

def process_files(input_dir, output_dir, pre_flags, post_flags, preview):
    output_dir.mkdir(parents=True, exist_ok=True)

    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
    
        if preview:
            # Output preview frame using ffmpeg
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = get_user_input()
    if input_dir is None or output_dir is None:
        return

    if not validate_directories(input_dir, output_dir):
        return

    if not validate_files(input_dir, output_dir):
        return

    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")

    start_time = None if len(start_time) == 0 else start_time
    duration = None if len(duration) == 0 else duration
    crop_params = None if len(crop_params) == 0 else [int(x) for x in crop_params.split(":") if x.isdigit()]
    crf = None if len(crf) == 0 else int(crf)

    pre_flags, post_flags = get_processing_flags(start_time, duration, crop_params, crf)

    if len(pre_flags) == 0 and len(post_flags) == 0:
        print("No flags specified")
        input("Press enter to exit")
        return

    preview = input("Generate preview thumbnails? (y/n): ").lower() == "y"

    process_files(input_dir, output_dir, pre_flags, post_flags, preview)

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

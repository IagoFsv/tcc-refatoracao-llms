"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def main():
    # Ask user for input and output directories
    input_dir = get_input_dir()
    output_dir = get_output_dir()

    # Check input directory exists
    check_input_dir_exists(input_dir)

    # Check for duplicate files in output directory
    check_output_dir_exists(input_dir, output_dir)

    # Ask user for start time and duration
    start_time, duration = get_time_params()
    start_flag, duration_flag = get_flags(start_time, duration)

    # Ask user for crop parameters
    crop_params = get_crop_params()
    crop_filter = get_crop_filter(crop_params)

    # Ask user for compression parameters
    crf = get_crf_level()
    compression_filter = get_compression_filter(crf)

    post_flags = f'{crop_filter} {compression_filter} {duration_flag}'.strip()

    if len(start_flag) == 0 and len(post_flags) == 0:
        print("No flags specified")
        input("Press enter to exit")
        return
    
    # Ask if user wants preview thumbnails
    preview = get_preview_option()

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file in the input directory
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {start_flag} -i {in_file} {post_flags} {out_file}")

        if preview:
            # Output preview frame using ffmpeg
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def get_input_dir():
    input_dir = input("Enter input directory: ")
    if len(input_dir) == 0:
        print("Input directory must be specified")
        input("Press enter to exit")
        return
    return Path(input_dir)

def check_input_dir_exists(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return

def check_output_dir_exists(input_dir, output_dir):
    if output_dir.exists():
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                print("Some files already exist in the output directory")
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite == "y":
                    print("Overwriting files")
                    return
                else:
                    print("Exiting")
                    input("Press enter to exit")
                    return

def get_time_params():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        start_time = None
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        duration = None
    return start_time, duration

# ... and so on for the rest of the methods

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

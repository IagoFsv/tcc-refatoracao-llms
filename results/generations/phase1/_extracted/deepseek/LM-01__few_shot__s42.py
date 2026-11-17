"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def main():
    # Ask user for input and output directories
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Check input directory exists
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return
    
    # Check for duplicate files in output directory
    if output_dir.exists():
        # Check if files in input exist in output directory
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                print("Some files already exist in the output directory")
                # Ask user if they want to overwrite files
                overwrite = input("Overwrite files?  (y/n): ")
                if overwrite == "y":
                    break
                else:
                    print("Exiting")
                    input("Press enter to exit")
                    return

    # Ask user for start time and duration
    start_time = ask_for_start_time()
    duration = ask_for_duration()

    # Ask user for crop parameters
    crop_params = ask_for_crop_params()

    # Ask user for compression parameters
    crf = ask_for_crf()

    # Ask if user wants preview thumbnails
    preview = ask_for_preview()

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file in the input directory
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        process_file(in_file, out_file, start_time, duration, crop_params, crf, preview)

def ask_for_start_time():
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        return None
    return start_time

def ask_for_duration():
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        return None
    return duration

def ask_for_crop_params():
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip): ")
    if len(crop_params) == 0:
        return None
    try:
        crop_params = crop_params.split(":")
        crop_params = [int(x) for x in crop_params]
        if len(crop_params) != 2 and len(crop_params) != 4:
            raise ValueError
        return crop_params
    except:
        print("Invalid crop parameters")
        input("Press enter to exit")
        return None

def ask_for_crf():
    crf = input("Enter crf level  (Enter nothing to skip): ")
    if len(crf) != 0:
        try:
            return int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    return None

def ask_for_preview():
    preview = input("Generate preview thumbnails?  (y/n): ")
    if preview == "y":
        return True
    return False

def process_file(in_file, out_file, start_time, duration, crop_params, crf, preview):
    pre_flags, post_flags = get_flags(start_time, duration, crop_params, crf)
    if len(pre_flags) == 0 and len(post_flags) == 0:
        print("No flags specified")
        input("Press enter to exit")
        return
    os.system(f"ffmpeg  -y {pre_flags} -i {in_file} {post_flags} {out_file}")
    if preview:
        # Output preview frame using ffmpeg
        os.system(f"ffmpeg  -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

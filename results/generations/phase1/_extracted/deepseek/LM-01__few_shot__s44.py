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
        check_for_duplicates(input_dir, output_dir)

    # Ask user for start time and duration
    start_time, duration = get_time_parameters()

    # Ask user for crop parameters
    crop_params = get_crop_parameters()

    # Ask user for compression parameters
    crf = get_compression_parameters()

    # Ask if user wants preview thumbnails
    preview = get_preview_option()

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file in the input directory
    for in_file in input_dir.iterdir():
        process_file(in_file, output_dir, start_time, duration, crop_params, crf, preview)

def check_for_duplicates(input_dir, output_dir):
    # Check if files in input exist in output directory
    for file in input_dir.iterdir():
        file_names = [x.name for x in output_dir.iterdir()]
        if file.name in file_names:
            print("Some files already exist in the output directory")
            # Ask user if they want to overwrite files
            overwrite = input("Overwrite files?  (y/n): ")
            if overwrite == "y":
                print("Overwriting files")
                break
            else:
                print("Exiting")
                input("Press enter to exit")
                return

def get_time_parameters():
    # Ask user for start time and duration
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip): ")
    return start_time, duration

def get_crop_parameters():
    # Ask user for crop parameters
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip): ")
    try:
        crop_params = crop_params.split(":")
        crop_params = [int(x) for x in crop_params]
        if len(crop_params) != 2 and len(crop_params) != 4:
            raise ValueError
    except:
        print("Invalid crop parameters")
        input("Press enter to exit")
        return
    return crop_params

def get_compression_parameters():
    # Ask user for compression parameters
    crf = input("Enter crf level  (Enter nothing to skip): ")
    try:
        crf = int(crf)
    except:
        print("Invalid crf level")
        input("Press enter to exit")
        return
    return crf

def get_preview_option():
    # Ask if user wants preview thumbnails
    preview = input("Generate preview thumbnails?  (y/n): ")
    if preview == "y":
        preview = True
    else:
        preview = False
    return preview

def process_file(in_file, output_dir, start_time, duration, crop_params, crf, preview):
    out_file = output_dir / in_file.name
    flags = get_flags(start_time, duration, crop_params, crf)
    os.system(f"ffmpeg  -y {flags} -i {in_file} {out_file}")
    if preview:
        # Output preview frame using ffmpeg
        os.system(f"ffmpeg  -y -i {out_file} -vframes 1 -f image2 {output_dir / (out_file.stem + '.jpg')}")

def get_flags(start_time, duration, crop_params, crf):
    start_flag = "-ss " + start_time if start_time is not None else ""
    duration_flag = "-t " + duration if duration is not None else ""
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params is not None else ""
    compression_filter = "-crf " + str(crf) if crf is not None else ""
    flags = start_flag + ' ' + crop_filter + ' ' + compression_filter + ' ' + duration_flag
    flags = flags.strip()
    return flags

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

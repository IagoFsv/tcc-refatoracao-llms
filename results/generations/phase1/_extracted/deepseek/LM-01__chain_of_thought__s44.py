"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os
from pathlib import Path

def ask_for_input_output_dir():
    # Ask user for input and output directories
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None

    return Path(input_dir), Path(output_dir)

def check_input_dir_exists(input_dir):
    # Check input directory exists
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def check_and_handle_output_dir(input_dir, output_dir):
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
                    print("Overwriting files")
                    return False
                else:
                    print("Exiting")
                    input("Press enter to exit")
                    return True
    return False

def ask_for_start_time_and_duration():
    # Ask user for start time and duration
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        start_time = None

    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        duration = None

    return start_time, duration

def create_ffmpeg_flags(start_time, duration):
    start_flag = ("-ss " + start_time) if start_time is not None else ""
    duration_flag = ("-t " + duration) if duration is not None else ""
    return start_flag, duration_flag

def ask_for_crop_parameters():
    # Ask user for crop parameters
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip): ")
    if len(crop_params) != 0:
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]

            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
        except:
            print("Invalid crop parameters")
            input("Press enter to exit")
            return None
    else:
        crop_params = None

    if crop_params is not None:
        crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params)
    else:
        crop_filter = ""

    return crop_filter

def ask_for_compression_parameters():
    # Ask user for compression parameters
    crf = input("Enter crf level  (Enter nothing to skip): ")
    if len(crf) != 0:
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    else:
        crf = None

    # Create compression filter if necessary
    if crf is not None:
        compression_filter = "-crf " + str(crf)
    else:
        compression_filter = ""

    return compression_filter

def ask_for_preview():
    # Ask if user wants preview thumbnails
    preview = input("Generate preview thumbnails?  (y/n): ")
    if preview == "y":
        return True
    else:
        return False

def create_output_dir(output_dir):
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

def process_files(input_dir, output_dir, start_flag, duration_flag, crop_filter, compression_filter, preview):
    # Process each file in the input directory
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg  -y {start_flag} {duration_flag} -i {in_file} {crop_filter} {compression_filter} {out_file}")
    
        if preview:
            # Output preview frame using ffmpeg
            os.system(f"ffmpeg  -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = ask_for_input_output_dir()
    if input_dir is None or output_dir is None:
        return

    if not check_input_dir_exists(input_dir):
        return

    if check_and_handle_output_dir(input_dir, output_dir):
        return

    start_time, duration = ask_for_start_time_and_duration()
    start_flag, duration_flag = create_ffmpeg_flags(start_time, duration)

    crop_filter = ask_for_crop_parameters()
    compression_filter = ask_for_compression_parameters()

    if crop_filter is None or compression_filter is None:
        return

    preview = ask_for_preview()

    create_output_dir(output_dir)

    process_files(input_dir, output_dir, start_flag, duration_flag, crop_filter, compression_filter, preview)

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

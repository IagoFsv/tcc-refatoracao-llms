"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def ask_user_for_input_directory():
    """Asks user for input directory."""
    return input("Enter input directory: ")

def ask_user_for_output_directory():
    """Asks user for output directory."""
    return input("Enter output directory: ")

def check_input_directory(input_dir):
    """Checks if input directory exists."""
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def check_duplicate_files(output_dir, input_dir):
    """Checks for duplicate files in output directory."""
    file_names = [x.name for x in output_dir.iterdir()]
    for file in input_dir.iterdir():
        if file.name in file_names:
            print("Some files already exist in the output directory")
            overwrite = input("Overwrite files? (y/n): ")
            if overwrite == "y":
                print("Overwriting files")
                break
            else:
                print("Exiting")
                input("Press enter to exit")
                return False
    return True

def ask_user_for_start_time_and_duration():
    """Asks user for start time and duration."""
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        start_time = None
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        duration = None
    return start_time, duration

def ask_user_for_crop_parameters():
    """Asks user for crop parameters."""
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
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
        return None

def ask_user_for_compression_parameters():
    """Asks user for compression parameters."""
    crf = input("Enter crf level (Enter nothing to skip): ")
    if len(crf) != 0:
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    else:
        return None

def ask_user_for_preview_thumbnails():
    """Asks user if they want preview thumbnails."""
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        return True
    else:
        return False

def process_file(in_file, out_file, start_time, duration, crop_params, compression_filter, preview):
    """Processes a file."""
    os.system(f"ffmpeg -y {' '.join(['-ss ' + start_time if start_time is not None else '', '-t ' + duration if duration is not None else ''])} -i {in_file} {' '.join([crop_filter if crop_params is not None else '', compression_filter if compression_filter is not None else '', duration_flag if duration is not None else ''])} {out_file}")
    if preview:
        os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def run():
    """Runs the converter. Public entry point of this unit."""
    input_dir = Path(ask_user_for_input_directory())
    output_dir = Path(ask_user_for_output_directory())

    if not check_input_directory(input_dir):
        return

    if not check_duplicate_files(output_dir, input_dir):
        return

    start_time, duration = ask_user_for_start_time_and_duration()
    crop_params = ask_user_for_crop_parameters()
    compression_filter = ask_user_for_compression_parameters()
    preview = ask_user_for_preview-thumbnails()

    output_dir.mkdir(parents=True, exist_ok=True)

    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        process_file(in_file, out_file, start_time, duration, crop_params, compression_filter, preview)

if __name__ == "__main__":
    run()

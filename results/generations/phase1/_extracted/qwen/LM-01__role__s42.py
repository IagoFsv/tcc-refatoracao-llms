"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def get_user_input():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    return input_dir, output_dir

def validate_user_input(input_dir, output_dir):
    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return False
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return input_dir, output_dir

def check_duplicate_files(input_dir, output_dir):
    if output_dir.exists():
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

def get_conversion_flags():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")
    return start_time, duration, crop_params, crf

def validate_conversion_flags(start_time, duration, crop_params, crf):
    start_flag = ("-ss " + start_time) if start_time is not None else ""
    duration_flag = ("-t " + duration) if duration is not None else ""
    crop_filter = ""
    compression_filter = ""
    if crop_params is not None:
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]
            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
            crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params)
        except:
            print("Invalid crop parameters")
            input("Press enter to exit")
            return None, None, None, None
    if crf is not None:
        try:
            crf = int(crf)
            compression_filter = "-crf " + str(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None, None, None, None
    return start_flag, duration_flag, crop_filter, compression_filter

def process_files(input_dir, output_dir, start_flag, duration_flag, crop_filter, compression_filter, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {start_flag} -i {in_file} {duration_flag} {crop_filter} {compression_filter} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = get_user_input()
    input_dir, output_dir = validate_user_input(input_dir, output_dir)
    if not input_dir or not output_dir:
        return
    if not check_duplicate_files(input_dir, output_dir):
        return
    start_time, duration, crop_params, crf = get_conversion_flags()
    start_flag, duration_flag, crop_filter, compression_filter = validate_conversion_flags(start_time, duration, crop_params, crf)
    if not start_flag or not duration_flag or not crop_filter or not compression_filter:
        return
    preview = input("Generate preview thumbnails? (y/n): ").lower() == "y"
    process_files(input_dir, output_dir, start_flag, duration_flag, crop_filter, compression_filter, preview)

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()


if __name__ == "__main__":
    run()

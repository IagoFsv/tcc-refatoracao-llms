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

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    return input_dir, output_dir

def validate_input(input_dir, output_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    
    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        for file in input_dir.iterdir():
            if file.name in file_names:
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite != "y":
                    print("Exiting")
                    input("Press enter to exit")
                    return False

    return True

def get_processing_flags():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")

    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")

    if crop_params:
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]
            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
        except:
            print("Invalid crop parameters")
            input("Press enter to exit")
            return None, None, None

        crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params)
    else:
        crop_filter = ""

    if crf:
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None, None, None

        compression_filter = "-crf " + str(crf)
    else:
        compression_filter = ""

    return start_flag, duration_flag, compression_filter

def process_files(input_dir, output_dir, start_flag, duration_flag, compression_filter):
    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()

    if not pre_flags and not post_flags:
        print("No flags specified")
        input("Press enter to exit")
        return

    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")

def generate_previews(output_dir):
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        for out_file in output_dir.iterdir():
            if out_file.is_file():
                os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = get_user_input()
    if input_dir is None or output_dir is None:
        return

    if not validate_input(input_dir, output_dir):
        return

    start_flag, duration_flag, compression_filter = get_processing_flags()
    if start_flag is None or duration_flag is None or compression_filter is None:
        return

    process_files(input_dir, output_dir, start_flag, duration_flag, compression_filter)
    generate_previews(output_dir)

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

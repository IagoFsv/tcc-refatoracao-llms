"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def get_user_inputs():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    return input_dir, output_dir

def check_directories(input_dir, output_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False

    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        for file in input_dir.iterdir():
            if file.name in file_names:
                print("Some files already exist in the output directory")
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite == "y":
                    print("Overwriting files")
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

    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    crop_params = crop_params.split(":") if crop_params else [None]
    crop_params = [int(x) for x in crop_params] if crop_params[0] else [None]
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params[0] else ""
    crf = int(crf) if crf else None
    compression_filter = "-crf " + str(crf) if crf else ""

    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()

    if not pre_flags and not post_flags:
        print("No flags specified")
        input("Press enter to exit")
        return None, None

    return pre_flags, post_flags

def generate_preview_thumbnails(output_dir, out_file):
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        preview = True
    else:
        preview = False

    if preview:
        os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {output_dir / (out_file.stem + '.jpg')}")

def process_files(input_dir, output_dir, pre_flags, post_flags):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")

def run():
    """Runs the converter. Public entry point of this unit."""
    input_dir, output_dir = get_user_inputs()
    if not input_dir or not output_dir:
        return

    if not check_directories(input_dir, output_dir):
        return

    pre_flags, post_flags = get_conversion_flags()
    if not pre_flags and not post_flags:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    process_files(input_dir, output_dir, pre_flags, post_flags)
    generate_preview_thumbnails(output_dir, out_file)


if __name__ == "__main__":
    run()

"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def ask_user_for_input_directory():
    while True:
        input_dir = input("Enter input directory: ")
        if len(input_dir) == 0:
            print("Input directory must be specified")
        else:
            return Path(input_dir)

def ask_user_for_output_directory():
    while True:
        output_dir = input("Enter output directory: ")
        if len(output_dir) == 0:
            print("Output directory must be specified")
        else:
            return Path(output_dir)

def check_input_directory(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def check_output_directory(output_dir):
    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        for file in output_dir.iterdir():
            if file.name in file_names:
                print("Some files already exist in the output directory")
                while True:
                    overwrite = input("Overwrite files? (y/n): ")
                    if overwrite == "y":
                        print("Overwriting files")
                        break
                    elif overwrite == "n":
                        print("Exiting")
                        input("Press enter to exit")
                        return False
                    else:
                        print("Invalid input, please try again")
        return True
    return True

def ask_user_for_start_time_and_duration():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        start_time = None
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        duration = None
    return start_time, duration

def ask_user_for_crop_parameters():
    while True:
        crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
        if len(crop_params) == 0:
            return None
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]
            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
        except:
            print("Invalid crop parameters")
        else:
            return crop_params

def ask_user_for_crf_level():
    while True:
        crf = input("Enter crf level (Enter nothing to skip): ")
        if len(crf) == 0:
            return None
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
        else:
            return crf

def ask_user_for_preview():
    while True:
        preview = input("Generate preview thumbnails? (y/n): ")
        if preview == "y":
            return True
        elif preview == "n":
            return False
        else:
            print("Invalid input, please try again")

def process_file(in_file, out_file, pre_flags, post_flags, preview):
    os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
    if preview:
        os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def run():
    """Runs the converter. Public entry point of this unit."""
    input_dir = ask_user_for_input_directory()
    output_dir = ask_user_for_output_directory()
    if not check_input_directory(input_dir) or not check_output_directory(output_dir):
        return
    start_time, duration = ask_user_for_start_time_and_duration()
    crop_params = ask_user_for_crop_parameters()
    crf = ask_user_for_crf_level()
    preview = ask_user_for_preview()
    output_dir.mkdir(parents=True, exist_ok=True)
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        pre_flags = f"-ss {start_time}" if start_time is not None else ""
        pre_flags += f" -t {duration}" if duration is not None else ""
        post_flags = ' '.join([f"-vf crop={':'.join(map(str, crop_params))}" if crop_params is not None else "", f"-crf {crf}" if crf is not None else "", f"-t {duration}" if duration is not None else ""])
        post_flags = post_flags.strip()
        if len(pre_flags) == 0 and len(post_flags) == 0:
            print("No flags specified")
            input("Press enter to exit")
            return
        process_file(in_file, out_file, pre_flags, post_flags, preview)

if __name__ == "__main__":
    run()

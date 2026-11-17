"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def ask_user_for_input():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    return input_dir, output_dir

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
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        start_time = None
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        duration = None
    return start_time, duration

def ask_user_for_crop_parameters():
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
        crop_params = None
    return crop_params

def ask_user_for_compression_parameters():
    crf = input("Enter crf level (Enter nothing to skip): ")
    if len(crf) != 0:
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    else:
        crf = None
    return crf

def create_flags(start_time, duration, crop_params, crf, duration_flag):
    pre_flags = "-ss " + start_time if start_time is not None else ""
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()
    if len(pre_flags) == 0 and len(post_flags) == 0:
        return None
    return pre_flags, post_flags

def ask_user_for_preview():
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        return True
    else:
        return False

def process_file(input_dir, output_dir, start_time, duration, crop_params, crf):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def run():
    """Runs the converter. Public entry point of this unit."""
    input_dir, output_dir = ask_user_for_input()
    if not check_input_directory(input_dir):
        return
    if not check_output_directory(output_dir):
        return
    start_time, duration = ask_user_for_start_time_and_duration()
    crop_params = ask_user_for_crop_parameters()
    crf = ask_user_for_compression_parameters()
    pre_flags, post_flags = create_flags(start_time, duration, crop_params, crf, duration_flag)
    preview = ask_user_for_preview()
    output_dir.mkdir(parents=True, exist_ok=True)
    process_file(input_dir, output_dir, start_time, duration, crop_params, crf)
    if preview:
        output_file = output_dir / (input_file.stem + '.jpg')
        os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {output_file}")

if __name__ == "__main__":
    run()

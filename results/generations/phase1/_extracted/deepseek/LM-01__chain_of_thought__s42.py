"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os
from pathlib import Path

def get_inputs():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    return Path(input_dir), Path(output_dir)

def check_input_dir(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def check_output_dir(output_dir):
    if output_dir.exists():
        print("Some files already exist in the output directory")
        overwrite = input("Overwrite files?  (y/n): ")
        if overwrite != "y":
            print("Exiting")
            input("Press enter to exit")
            return False
    return True

def get_flags():
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level  (Enter nothing to skip): ")
    return start_time, duration, crop_params, crf

def check_crop_params(crop_params):
    if len(crop_params) != 0:
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
    return None

def check_crf(crf):
    if len(crf) != 0:
        try:
            return int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    return None

def process_files(input_dir, output_dir, start_time, duration, crop_params, crf):
    pre_flags, post_flags = get_flags(start_time, duration, crop_params, crf)
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg  -y {pre_flags} -i {in_file} {post_flags} {out_file}")

def generate_preview(output_dir):
    preview = input("Generate preview thumbnails?  (y/n): ")
    if preview == "y":
        for out_file in output_dir.iterdir():
            os.system(f"ffmpeg  -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = get_inputs()
    if not check_input_dir(input_dir):
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    if not check_output_dir(output_dir):
        return
    start_time, duration, crop_params, crf = get_flags()
    crop_params = check_crop_params(crop_params)
    crf = check_crf(crf)
    process_files(input_dir, output_dir, start_time, duration, crop_params, crf)
    generate_preview(output_dir)

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

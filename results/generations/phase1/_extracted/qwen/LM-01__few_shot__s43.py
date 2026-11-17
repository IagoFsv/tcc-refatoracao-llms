"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os

from pathlib import Path

def _get_user_input():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    return input_dir, output_dir

def _validate_directories(input_dir, output_dir):
    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return False
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    return input_dir, output_dir

def _check_input_directory(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def _check_output_directory(output_dir):
    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        for file in input_dir.iterdir():
            if file.name in file_names:
                print("Some files already exist in the output directory")
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite != "y":
                    print("Exiting")
                    input("Press enter to exit")
                    return False
    return True

def _get_time_and_duration():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    return start_flag, duration_flag

def _get_crop_parameters():
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    if len(crop_params) != 0:
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]
            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
        except ValueError:
            print("Invalid crop parameters")
            input("Press enter to exit")
            return None
    return crop_params

def _build_crop_filter(crop_params):
    if crop_params is not None:
        return "-vf crop=" + ":".join(str(x) for x in crop_params)
    return ""

def _get_crf_level():
    crf = input("Enter crf level (Enter nothing to skip): ")
    if len(crf) != 0:
        try:
            crf = int(crf)
        except ValueError:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    return crf

def _build_compression_filter(crf):
    if crf is not None:
        return "-crf " + str(crf)
    return ""

def _get_pre_and_post_flags(start_flag, duration_flag, crop_filter, compression_filter):
    pre_flags = start_flag
    post_flags = ' '.join(filter(None, [crop_filter, compression_filter, duration_flag]))
    return pre_flags, post_flags

def _ask_for_preview():
    preview = input("Generate preview thumbnails? (y/n): ")
    return preview.lower() == "y"

def _create_output_directory(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

def _process_files(input_dir, output_dir, pre_flags, post_flags, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = _get_user_input()
    input_dir, output_dir = _validate_directories(input_dir, output_dir)
    if not input_dir or not output_dir:
        return
    if not _check_input_directory(input_dir) or not _check_output_directory(output_dir):
        return
    start_flag, duration_flag = _get_time_and_duration()
    crop_params = _get_crop_parameters()
    crop_filter = _build_crop_filter(crop_params)
    crf = _get_crf_level()
    compression_filter = _build_compression_filter(crf)
    pre_flags, post_flags = _get_pre_and_post_flags(start_flag, duration_flag, crop_filter, compression_filter)
    preview = _ask_for_preview()
    _create_output_directory(output_dir)
    _process_files(input_dir, output_dir, pre_flags, post_flags, preview)

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

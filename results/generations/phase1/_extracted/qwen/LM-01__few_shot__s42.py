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

def _validate_input_output(input_dir, output_dir):
    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return False
    return True

def _get_input_directory(input_dir):
    input_dir = Path(input_dir)
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def _check_duplicate_files(output_dir):
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

def _get_time_and_duration():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    return start_time, duration

def _validate_time_and_duration(start_time, duration):
    if len(start_time) == 0:
        start_time = None
    else:
        try:
            start_time = start_time.split(":")
            start_time = [int(x) for x in start_time]
            if len(start_time) != 3:
                raise ValueError
        except:
            print("Invalid start time")
            input("Press enter to exit")
            return False

    if len(duration) == 0:
        duration = None
    else:
        try:
            duration = duration.split(":")
            duration = [int(x) for x in duration]
            if len(duration) != 3:
                raise ValueError
        except:
            print("Invalid duration")
            input("Press enter to exit")
            return False

    return True

def _get_crop_params():
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    return crop_params

def _validate_crop_params(crop_params):
    if len(crop_params) != 0:
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]
            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
        except:
            print("Invalid crop parameters")
            input("Press enter to exit")
            return False
    return True

def _get_crf():
    crf = input("Enter crf level (Enter nothing to skip): ")
    return crf

def _validate_crf(crf):
    if len(crf) != 0:
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return False
    return True

def _build_ffmpeg_flags(start_time, duration, crop_params, crf):
    start_flag = ("-ss " + start_time) if start_time is not None else ""
    duration_flag = ("-t " + duration) if duration is not None else ""
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params is not None else ""
    compression_filter = "-crf " + str(crf) if crf is not None else ""
    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()
    return pre_flags, post_flags

def _ask_for_preview():
    preview = input("Generate preview thumbnails? (y/n): ")
    return preview == "y"

def _create_output_directory(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

def _process_file(in_file, out_file, pre_flags, post_flags):
    os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")

def _generate_preview_thumbnails(out_file):
    os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = _get_user_input()
    if not _validate_input_output(input_dir, output_dir):
        return
    if not _get_input_directory(input_dir):
        return
    if not _check_duplicate_files(output_dir):
        return
    start_time, duration = _get_time_and_duration()
    if not _validate_time_and_duration(start_time, duration):
        return
    crop_params = _get_crop_params()
    if not _validate_crop_params(crop_params):
        return
    crf = _get_crf()
    if not _validate_crf(crf):
        return
    pre_flags, post_flags = _build_ffmpeg_flags(start_time, duration, crop_params, crf)
    preview = _ask_for_preview()
    _create_output_directory(output_dir)
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        _process_file(in_file, out_file, pre_flags, post_flags)
        if preview:
            _generate_preview_thumbnails(out_file)

def run():
    """Runs the converter. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()

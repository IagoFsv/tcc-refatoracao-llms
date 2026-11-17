"""Batch video converter with ffmpeg.

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

import os
from pathlib import Path


def ask_user_input():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    return input_dir, output_dir


def check_input_directory(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return


def check_output_directory(input_dir, output_dir):
    if output_dir.exists():
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                print("Some files already exist in the output directory")
                overwrite = input("Overwrite files?  (y/n): ")
                if overwrite == "y":
                    print("Overwriting files")
                    return True
                else:
                    print("Exiting")
                    input("Press enter to exit")
                    return False


def ask_for_start_and_duration():
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip): ")

    if len(start_time) == 0:
        start_time = None

    if len(duration) == 0:
        duration = None

    return start_time, duration


def ask_for_crop_parameters():
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
            return
    else:
        crop_params = None

    return crop_params


def ask_for_compression_parameters():
    crf = input("Enter crf level  (Enter nothing to skip): ")

    if len(crf) != 0:
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return
    else:
        crf = None

    return crf


def generate_ffmpeg_flags(start_time, duration, crop_params, crf):
    start_flag = "-ss " + start_time if start_time is not None else ""
    duration_flag = "-t " + duration if duration is not None else ""

    if crop_params is not None:
        crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params)
    else:
        crop_filter = ""

    if crf is not None:
        compression_filter = "-crf " + str(crf)
    else:
        compression_filter = ""

    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag]).strip()

    if len(pre_flags) == 0 and len(post_flags) == 0:
        print("No flags specified")
        input("Press enter to exit")
        return

    return pre_flags, post_flags


def ask_for_preview():
    preview = input("Generate preview thumbnails?  (y/n): ")
    if preview == "y":
        return True
    else:
        return False


def create_output_directory(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)


def process_files(input_dir, output_dir, pre_flags, post_flags, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg  -y {pre_flags} -i {in_file} {post_flags} {out_file}")

        if preview:
            os.system(f"ffmpeg  -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")


def main():
    input_dir, output_dir = ask_user_input()

    check_input_directory(input_dir)

    if check_output_directory(input_dir, output_dir):
        start_time, duration = ask_for_start_and_duration()
        crop_params = ask_for_crop_parameters()
        crf = ask_for_compression_parameters()
        pre_flags, post_flags = generate_ffmpeg_flags(start_time, duration, crop_params, crf)
        preview = ask_for_preview()
        create_output_directory(output_dir)
        process_files(input_dir, output_dir, pre_flags, post_flags, preview)


def run():
    """Runs the converter. Public entry point of this unit."""
    return main()


if __name__ == "__main__":
    run()

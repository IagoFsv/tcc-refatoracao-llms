import os
from pathlib import Path

def get_user_input():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    return input_dir, output_dir

def validate_directories(input_dir, output_dir):
    if not input_dir or not output_dir:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return False
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        if any(file.name in file_names for file in input_dir.iterdir()):
            overwrite = input("Overwrite files? (y/n): ")
            if overwrite != "y":
                print("Exiting")
                input("Press enter to exit")
                return False
    return True

def get_time_and_duration():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    return start_time, duration

def get_crop_params():
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    return crop_params

def get_compression_params():
    crf = input("Enter crf level (Enter nothing to skip): ")
    return crf

def create_filters(start_time, duration, crop_params, crf):
    pre_flags = f"-ss {start_time}" if start_time else ""
    duration_flag = f"-t {duration}" if duration else ""
    crop_filter = f"-vf crop={crop_params}" if crop_params else ""
    compression_filter = f"-crf {crf}" if crf else ""
    post_flags = ' '.join(filter(None, [pre_flags, crop_filter, compression_filter, duration_flag]))
    return pre_flags, post_flags

def create_output_directory(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

def process_files(input_dir, output_dir, pre_flags, post_flags, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def executar():
    input_dir, output_dir = get_user_input()
    if not validate_directories(input_dir, output_dir):
        return
    start_time, duration = get_time_and_duration()
    crop_params = get_crop_params()
    crf = get_compression_params()
    pre_flags, post_flags = create_filters(start_time, duration, crop_params, crf)
    preview = input("Generate preview thumbnails? (y/n): ").lower() == "y"
    create_output_directory(output_dir)
    process_files(input_dir, output_dir, pre_flags, post_flags, preview)

if __name__ == "__main__":
    executar()

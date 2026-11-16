import os
from pathlib import Path

def get_user_input():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    return input_dir, output_dir

def validate_directories(input_dir, output_dir):
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
    return True

def check_duplicate_files(input_dir, output_dir):
    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        for file in input_dir.iterdir():
            if file.name in file_names:
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite == "y":
                    print("Overwriting files")
                    return True
                else:
                    print("Exiting")
                    input("Press enter to exit")
                    return False
    return True

def get_time_and_duration():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    return start_flag, duration_flag

def get_crop_parameters():
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    if len(crop_params):
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]
            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
        except:
            print("Invalid crop parameters")
            input("Press enter to exit")
            return None
    return crop_params

def get_compression_parameters():
    crf = input("Enter crf level (Enter nothing to skip): ")
    if len(crf):
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    return crf

def create_filters(pre_flags, post_flags):
    if pre_flags or post_flags:
        return pre_flags, post_flags
    print("No flags specified")
    input("Press enter to exit")
    return None, None

def get_preview_option():
    preview = input("Generate preview thumbnails? (y/n): ")
    return preview == "y"

def create_output_directory(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

def process_files(input_dir, output_dir, pre_flags, post_flags, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = get_user_input()
    if not validate_directories(input_dir, output_dir):
        return
    if not check_duplicate_files(input_dir, output_dir):
        return
    start_flag, duration_flag = get_time_and_duration()
    crop_params = get_crop_parameters()
    crf = get_compression_parameters()
    pre_flags, post_flags = create_filters(start_flag, ' '.join([f"-vf crop={'x:y:w:h' if crop_params else ''}", f"-crf {crf}" if crf else ''], duration_flag))
    preview = get_preview_option()
    create_output_directory(output_dir)
    process_files(input_dir, output_dir, pre_flags, post_flags, preview)

def executar():
    return main()

if __name__ == "__main__":
    executar()

import os

from pathlib import Path

def ask_user_for_input_and_output():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return input_dir, output_dir
    return Path(input_dir), Path(output_dir)

def check_input_directory(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def check_for_duplicate_files(output_dir):
    if output_dir.exists():
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
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
        return None

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
        return None

def ask_user_for_preview():
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        return True
    else:
        return False

def process_each_file(input_dir, output_dir):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = ask_user_for_input_and_output()
    if not check_input_directory(input_dir):
        return
    if not check_for_duplicate_files(output_dir):
        return
    start_time, duration = ask_user_for_start_time_and_duration()
    crop_params = ask_user_for_crop_parameters()
    crf = ask_user_for_compression_parameters()
    preview = ask_user_for_preview()
    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()
    if len(pre_flags) == 0 and len(post_flags) == 0:
        print("No flags specified")
        input("Press enter to exit")
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    process_each_file(input_dir, output_dir)

if __name__ == "__main__":
    main()

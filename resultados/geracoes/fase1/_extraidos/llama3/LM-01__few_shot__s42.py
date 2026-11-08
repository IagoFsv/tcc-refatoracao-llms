def ask_user_for_input_and_output_directories():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None
    return Path(input_dir), Path(output_dir)

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

def ask_user_for_crf_level():
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

def ask_user_for_preview():
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        preview = True
    else:
        preview = False
    return preview

def process_file(input_dir, output_dir, start_time, duration, crop_params, crf, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y -i {in_file} -vf crop={crop_filter} -crf {crf} -t {duration} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = ask_user_for_input_and_output_directories()
    if input_dir is None or output_dir is None:
        return
    if not check_input_directory(input_dir):
        return
    if not check_output_directory(output_dir):
        return
    start_time, duration = ask_user_for_start_time_and_duration()
    crop_params = ask_user_for_crop_parameters()
    crf = ask_user_for_crf_level()
    preview = ask_user_for_preview()
    output_dir.mkdir(parents=True, exist_ok=True)
    process_file(input_dir, output_dir, start_time, duration, crop_params, crf, preview)

if __name__ == "__main__":
    main()

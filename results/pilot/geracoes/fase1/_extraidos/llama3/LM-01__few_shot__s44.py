def ask_input_directory():
    while True:
        input_dir = input("Enter input directory: ")
        if len(input_dir) == 0:
            print("Input directory must be specified")
        else:
            return Path(input_dir)

def ask_output_directory():
    while True:
        output_dir = input("Enter output directory: ")
        if len(output_dir) == 0:
            print("Output directory must be specified")
        else:
            return Path(output_dir)

def check_input_directory(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        return False
    return True

def check_output_directory(output_dir):
    if output_dir.exists():
        for file in output_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                print("Some files already exist in the output directory")
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite == "y":
                    print("Overwriting files")
                    return True
                else:
                    print("Exiting")
                    return False
    return True

def ask_start_time():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        return None
    return start_time

def ask_duration():
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        return None
    return duration

def ask_crop_params():
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    if len(crop_params) == 0:
        return None
    try:
        crop_params = crop_params.split(":")
        crop_params = [int(x) for x in crop_params]
        if len(crop_params) != 2 and len(crop_params) != 4:
            raise ValueError
        return crop_params
    except:
        print("Invalid crop parameters")
        return None

def ask_crf_level():
    crf = input("Enter crf level (Enter nothing to skip): ")
    if len(crf) == 0:
        return None
    try:
        crf = int(crf)
        return crf
    except:
        print("Invalid crf level")
        return None

def ask_preview():
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        return True
    else:
        return False

def process_file(in_file, out_file, start_time, duration, crop_params, crf, preview):
    os.system(f"ffmpeg -y {'-ss ' + start_time if start_time is not None else ''} {'-t ' + duration if duration is not None else ''} {'-vf crop=' + ':'.join(str(x) for x in crop_params) if crop_params is not None else ''} {'-crf ' + str(crf) if crf is not None else ''} -i {in_file} {out_file}")

def main():
    input_dir = ask_input_directory()
    output_dir = ask_output_directory()
    if not check_input_directory(input_dir):
        return
    if not check_output_directory(output_dir):
        return
    start_time = ask_start_time()
    duration = ask_duration()
    crop_params = ask_crop_params()
    crf = ask_crf_level()
    preview = ask_preview()
    output_dir.mkdir(parents=True, exist_ok=True)
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        process_file(in_file, out_file, start_time, duration, crop_params, crf, preview)
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def executar():
    return main()

if __name__ == "__main__":
    executar()

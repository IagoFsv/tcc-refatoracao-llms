def _validate_input(input_dir, output_dir):
    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return False
    return True

def _check_output_directory(input_dir, output_dir):
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

def _get_start_time_and_duration():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    if len(start_time) == 0:
        start_time = None
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    if len(duration) == 0:
        duration = None
    return start_time, duration

def _get_crop_parameters():
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

def _get_crf():
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

def _ask_preview():
    preview = input("Generate preview thumbnails? (y/n): ")
    if preview == "y":
        return True
    else:
        return False

def _process_file(in_file, out_file, pre_flags, post_flags, preview):
    os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
    if preview:
        os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    if not _validate_input(input_dir, output_dir):
        return
    if not _check_output_directory(input_dir, output_dir):
        return
    start_time, duration = _get_start_time_and_duration()
    crop_params = _get_crop_parameters()
    crf = _get_crf()
    preview = _ask_preview()
    output_dir.mkdir(parents=True, exist_ok=True)
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        pre_flags = f"-ss {start_time}" if start_time is not None else ""
        post_flags = ' '.join([f"-vf crop={crop_params[0]}:{crop_params[1]}:{crop_params[2]}:{crop_params[3]}" if crop_params is not None else "", f"-crf {crf}" if crf is not None else "", f"-t {duration}" if duration is not None else ""])
        post_flags = post_flags.strip()
        _process_file(in_file, out_file, pre_flags, post_flags, preview)

def executar():
    return main()

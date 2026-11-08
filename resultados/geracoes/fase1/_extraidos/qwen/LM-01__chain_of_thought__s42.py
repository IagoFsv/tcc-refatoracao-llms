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
    return input_dir, output_dir

def get_time_and_duration():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    return start_flag, duration_flag

def get_crop_parameters():
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    if crop_params:
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

def get_compression_parameters():
    crf = input("Enter crf level (Enter nothing to skip): ")
    if crf:
        try:
            crf = int(crf)
        except ValueError:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    return crf

def create_ffmpeg_flags(start_flag, duration_flag, crop_params, crf):
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params else ""
    compression_filter = "-crf " + str(crf) if crf is not None else ""
    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()
    return pre_flags, post_flags

def process_files(input_dir, output_dir, pre_flags, post_flags, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = get_user_input()
    input_dir, output_dir = validate_directories(input_dir, output_dir)
    start_flag, duration_flag = get_time_and_duration()
    crop_params = get_crop_parameters()
    crf = get_compression_parameters()
    pre_flags, post_flags = create_ffmpeg_flags(start_flag, duration_flag, crop_params, crf)
    preview = input("Generate preview thumbnails? (y/n): ").lower() == "y"
    output_dir.mkdir(parents=True, exist_ok=True)
    process_files(input_dir, output_dir, pre_flags, post_flags, preview)

def executar():
    """Executa o conversor. Ponto de entrada público desta unidade."""
    return main()

if __name__ == "__main__":
    executar()

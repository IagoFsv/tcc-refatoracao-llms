import os
from pathlib import Path

def ask_user_for_input_and_output_dirs():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    # ... (rest of the code remains the same)

def check_input_directory(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def check_for_duplicate_files(input_dir, output_dir):
    # ... (rest of the code remains the same)

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
        return None

def create_compression_filter(crf):
    if crf is not None:
        return f"-crf {crf}"
    else:
        return ""

def create_output_directory(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

def process_file(input_dir, output_dir, in_file):
    out_file = output_dir / in_file.name
    os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")

def generate_preview_thumbnail(out_file):
    os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    # ... (rest of the code remains the same)

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == "__main__":
    executar()

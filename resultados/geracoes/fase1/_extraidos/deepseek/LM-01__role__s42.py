"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os
from pathlib import Path

def main():
    # Ask user for input and output directories
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Check input directory exists
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return

    check_duplicate_files(output_dir)
    start_time, duration, crop_params, crf = get_user_input()
    pre_flags, post_flags, compression_filter, crop_filter = get_flags(start_time, duration, crop_params, crf)
    preview = get_preview_input()
    create_output_dir(output_dir)
    process_files(input_dir, output_dir, pre_flags, post_flags, compression_filter, crop_filter, preview)

def check_duplicate_files(output_dir):
    # Check for duplicate files in output directory
    if output_dir.exists():
        # Check if files in input exist in output directory
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                handle_duplicate_files()

def get_user_input():
    # Ask user for start time and duration
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level  (Enter nothing to skip): ")
    return start_time, duration, crop_params, crf

def get_flags(start_time, duration, crop_params, crf):
    # Create flags
    pre_flags = get_start_flag(start_time)
    post_flags, compression_filter, crop_filter = get_post_flags(duration, crop_params, crf)
    return pre_flags, post_flags, compression_filter, crop_filter

def get_start_flag(start_time):
    return ("-ss " + start_time) if start_time is not None else ""

def get_post_flags(duration, crop_params, crf):
    crop_filter, compression_filter = "", ""
    if crop_params is not None:
        crop_filter = get_crop_filter(crop_params)
    if crf is not None:
        compression_filter = get_compression_filter(crf)
    post_flags = ' '.join([crop_filter, compression_filter, get_duration_flag(duration)])
    post_flags = post_flags.strip()
    return post_flags, compression_filter, crop_filter

def get_crop_filter(crop_params):
    return "-vf crop=" + ":".join(str(x) for x in crop_params)

def get_compression_filter(crf):
    return "-crf " + str(crf)

def get_duration_flag(duration):
    return "-t " + duration if duration is not None else ""

def get_preview_input():
    # Ask if user wants preview thumbnails
    preview = input("Generate preview thumbnails?  (y/n): ")
    return True if preview == "y" else False

def create_output_dir(output_dir):
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

def process_files(input_dir, output_dir, pre_flags, post_flags, compression_filter, crop_filter, preview):
    # Process each file in the input directory
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            # Output preview frame using ffmpeg
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == "__main__":
    executar()

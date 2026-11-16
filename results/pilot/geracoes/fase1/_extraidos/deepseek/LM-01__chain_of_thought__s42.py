"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os
from pathlib import Path

def main():
    # Ask user for input and output directories
    input_dir = input("Enter input directory:  ")
    output_dir = input("Enter output directory:  ")

    validate_directories(input_dir, output_dir)

    # Check for duplicate files in output directory
    check_for_duplicates(input_dir, output_dir)

    # Ask user for start time and duration
    start_time, duration = get_start_and_duration()

    # Ask user for crop parameters
    crop_params = get_crop_parameters()

    # Ask user for compression parameters
    crf = get_compression_parameters()

    # Ask if user wants preview thumbnails
    preview = get_preview_option()

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file in the input directory
    process_files(input_dir, output_dir, start_time, duration, crop_params, crf, preview)

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()

def validate_directories(input_dir, output_dir):
    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        exit()

def check_for_duplicates(input_dir, output_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        exit()

def get_start_and_duration():
    # Ask user for start time and duration
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip):  ")
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip):  ")

    return start_time, duration

def get_crop_parameters():
    # Ask user for crop parameters
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip):  ")

    return crop_params

def get_compression_parameters():
    # Ask user for compression parameters
    crf = input("Enter crf level  (Enter nothing to skip):  ")

    return crf

def get_preview_option():
    # Ask if user wants preview thumbnails
    preview = input("Generate preview thumbnails?  (y/n):  ")
    if preview == "y":
        preview = True
    else:
        preview = False

    return preview

def process_files(input_dir, output_dir, start_time, duration, crop_params, crf, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg  -y -i {in_file} -o {out_file}")

        if preview:
            # Output preview frame using ffmpeg
            os.system(f"ffmpeg  -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

if __name__ == "__main__":
    executar()

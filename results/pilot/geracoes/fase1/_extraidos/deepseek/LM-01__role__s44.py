"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os
from pathlib import Path

def get_user_input():
    # Ask user for input and output directories
    input_dir = input("Enter input directory:  ")
    output_dir = input("Enter output directory:  ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None

    return Path(input_dir), Path(output_dir)

def check_input_directory(input_dir):
    # Check input directory exists
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False
    return True

def check_output_directory(output_dir, input_dir):
    # Check for duplicate files in output directory
    if output_dir.exists():
        # Check if files in input exist in output directory
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                print("Some files already exist in the output directory")
                # Ask user if they want to overwrite files
                overwrite = input("Overwrite files?  (y/n):  ")
                if overwrite == "y":
                    print("Overwriting files")
                    return True
                else:
                    print("Exiting")
                    input("Press enter to exit")
                    return False
    return True

def get_processing_parameters():
    # Ask user for start time and duration
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip):  ")
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip):  ")

    # Ask user for crop parameters
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip):  ")
    # Ask user for compression parameters
    crf = input("Enter crf level  (Enter nothing to skip):  ")

    # Ask if user wants preview thumbnails
    preview = input("Generate preview thumbnails?  (y/n):  ")
    return start_time, duration, crop_params, crf, preview

def process_files(input_dir, output_dir, start_time, duration, crop_params, crf, preview):
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file in the input directory
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg  -y  -i {in_file}  {out_file}")

        if preview == "y":
            # Output preview frame using ffmpeg
            os.system(f"ffmpeg  -y  -i {out_file}  -vframes 1  -f image2  {out_file.parent / (out_file.stem + '.jpg')}")

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    input_dir, output_dir = get_user_input()
    if input_dir is None:
        return
    if not check_input_directory(input_dir):
        return
    if not check_output_directory(output_dir, input_dir):
        return
    start_time, duration, crop_params, crf, preview = get_processing_parameters()
    process_files(input_dir, output_dir, start_time, duration, crop_params, crf, preview)

if __name__ == "__main__":
    executar()

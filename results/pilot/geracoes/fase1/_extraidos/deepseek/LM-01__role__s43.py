"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os
from pathlib import Path

def main():
    user_input()
    check_directories()
    ask_for_flags()
    check_crop_params()
    check_compression_params()
    ask_for_preview()
    create_output_directory()
    process_files()

def user_input():
    global input_dir, output_dir, start_time, duration, crop_params, crf
    input_dir = Path(input("Enter input directory: "))
    output_dir = Path(input("Enter output directory: "))
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration  (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters  (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level  (Enter nothing to skip): ")

def check_directories():
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        exit()

def ask_for_flags():
    global start_flag, duration_flag, crop_filter, compression_filter
    start_flag = " -ss " + start_time if start_time else ""
    duration_flag = " -t " + duration if duration else ""
    crop_filter = " -vf crop=" + ":".join(crop_params) if crop_params else ""
    compression_filter = " -crf " + crf if crf else ""
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag]).strip()
    if not (start_flag or post_flags):
        print("No flags specified")
        input("Press enter to exit")
        exit()

def check_crop_params():
    if not crop_params:
        return
    try:
        crop_params = crop_params.split(":")
        crop_params = [int(x) for x in crop_params]
        if len(crop_params) not in [2, 4]:
            raise ValueError
    except:
        print("Invalid crop parameters")
        input("Press enter to exit")
        exit()

def check_compression_params():
    if not crf:
        return
    try:
        crf = int(crf)
    except:
        print("Invalid crf level")
        input("Press enter to exit")
        exit()

def ask_for_preview():
    global preview
    preview = input("Generate preview thumbnails?  (y/n): ") == "y"

def create_output_directory():
    if preview and output_dir.exists():
        for file in input_dir.iterdir():
            if file.name in [x.name for x in output_dir.iterdir()]:
                print("Some files already exist in the output directory")
                overwrite = input("Overwrite files?  (y/n): ")
                if overwrite != "y":
                    print("Exiting")
                    input("Press enter to exit")
                    exit()
    output_dir.mkdir(parents=True, exist_ok=True)

def process_files():
    global preview
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {start_flag} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {output_dir / (out_file.stem + '.jpg')}")

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == "__main__":
    executar()

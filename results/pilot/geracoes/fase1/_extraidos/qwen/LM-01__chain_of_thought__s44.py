import os
from pathlib import Path

def obter_diretorios():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    return input_dir, output_dir

def verificar_diretorios(input_dir, output_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False

    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        for file in input_dir.iterdir():
            if file.name in file_names:
                print("Some files already exist in the output directory")
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite != "y":
                    print("Exiting")
                    input("Press enter to exit")
                    return False

    return True

def obter_parametros_usuario():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")

    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    crop_params = [int(x) for x in crop_params.split(":")] if crop_params else None
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params else ""
    crf = int(crf) if crf else None
    compression_filter = "-crf " + str(crf) if crf else ""

    return start_flag, duration_flag, crop_filter, compression_filter

def criar_filtro(pre_flags, post_flags):
    pre_flags = pre_flags
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag]).strip()
    return pre_flags, post_flags

def gerar_thumbnails(preview, out_file):
    if preview:
        os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def processar_arquivos(input_dir, output_dir, pre_flags, post_flags):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        gerar_thumbnails(preview, out_file)

def main():
    input_dir, output_dir = obter_diretorios()
    if not input_dir or not output_dir:
        return

    if not verificar_diretorios(input_dir, output_dir):
        return

    start_flag, duration_flag, crop_filter, compression_filter = obter_parametros_usuario()
    pre_flags, post_flags = criar_filtro(start_flag, duration_flag, crop_filter, compression_filter)

    if not pre_flags and not post_flags:
        print("No flags specified")
        input("Press enter to exit")
        return

    preview = input("Generate preview thumbnails? (y/n): ").lower() == "y"
    processar_arquivos(input_dir, output_dir, pre_flags, post_flags)

def executar():
    return main()

if __name__ == "__main__":
    executar()

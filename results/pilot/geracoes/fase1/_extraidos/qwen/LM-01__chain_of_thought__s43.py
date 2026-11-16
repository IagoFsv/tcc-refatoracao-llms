import os
from pathlib import Path

def obter_diretorios():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    return input_dir, output_dir

def validar_diretorios(input_dir, output_dir):
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
    return True

def obter_parametros():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")
    return start_time, duration, crop_params, crf

def processar_parametros(start_time, duration, crop_params, crf):
    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    crop_filter = f"-vf crop={':'.join(str(x) for x in crop_params)}" if crop_params else ""
    compression_filter = f"-crf {crf}" if crf else ""
    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag]).strip()
    return pre_flags, post_flags

def processar_arquivos(input_dir, output_dir, pre_flags, post_flags, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = obter_diretorios()
    if not validar_diretorios(input_dir, output_dir):
        return
    start_time, duration, crop_params, crf = obter_parametros()
    pre_flags, post_flags = processar_parametros(start_time, duration, crop_params, crf)
    preview = input("Generate preview thumbnails? (y/n): ").lower() == 'y'
    processar_arquivos(input_dir, output_dir, pre_flags, post_flags, preview)

def executar():
    return main()

if __name__ == "__main__":
    executar()

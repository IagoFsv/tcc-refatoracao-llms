import os
from pathlib import Path

def _obter_diretorios():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")
    if len(input_dir) == 0 or len(output_dir) == 0:
        raise ValueError("Input and output directories must be specified")
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    return input_dir, output_dir

def _validar_diretorios(input_dir, output_dir):
    if not input_dir.exists():
        raise ValueError("Input directory does not exist")
    if output_dir.exists():
        file_names = [x.name for x in output_dir.iterdir()]
        for file in input_dir.iterdir():
            if file.name in file_names:
                overwrite = input("Overwrite files? (y/n): ")
                if overwrite != "y":
                    raise ValueError("Exiting")

def _obter_parametros():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")
    return start_time, duration, crop_params, crf

def _validar_parametros(start_time, duration, crop_params, crf):
    start_flag = ("-ss " + start_time) if start_time else ""
    duration_flag = ("-t " + duration) if duration else ""
    crop_params = crop_params.split(":") if crop_params else None
    crf = int(crf) if crf else None
    return start_flag, duration_flag, crop_params, crf

def _criar_filtro(crop_params, crf):
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params else ""
    compression_filter = "-crf " + str(crf) if crf else ""
    return crop_filter, compression_filter

def _processar_arquivos(input_dir, output_dir, start_flag, duration_flag, crop_filter, compression_filter):
    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag]).strip()
    if len(pre_flags) == 0 and len(post_flags) == 0:
        raise ValueError("No flags specified")
    preview = input("Generate preview thumbnails? (y/n): ").lower() == "y"
    output_dir.mkdir(parents=True, exist_ok=True)
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = _obter_diretorios()
    _validar_diretorios(input_dir, output_dir)
    start_time, duration, crop_params, crf = _obter_parametros()
    start_flag, duration_flag, crop_params, crf = _validar_parametros(start_time, duration, crop_params, crf)
    crop_filter, compression_filter = _criar_filtro(crop_params, crf)
    _processar_arquivos(input_dir, output_dir, start_flag, duration_flag, crop_filter, compression_filter)

def executar():
    return main()

if __name__ == "__main__":
    executar()

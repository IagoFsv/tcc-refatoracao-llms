import os
from pathlib import Path

def _obter_diretorios():
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    return input_dir, output_dir

def _validar_diretorio(input_dir):
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return False

    return True

def _verificar_duplicatas(output_dir, input_dir):
    file_names = [x.name for x in output_dir.iterdir()]
    for file in input_dir.iterdir():
        if file.name in file_names:
            print("Some files already exist in the output directory")
            overwrite = input("Overwrite files? (y/n): ")
            if overwrite == "y":
                print("Overwriting files")
                return False
            else:
                print("Exiting")
                input("Press enter to exit")
                return False
    return True

def _obter_parametros_avançados():
    start_time = input("Enter start time (HH:MM:SS, enter nothing to skip): ")
    duration = input("Enter duration (HH:MM:SS, enter nothing to skip): ")
    crop_params = input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")
    crf = input("Enter crf level (Enter nothing to skip): ")

    return start_time, duration, crop_params, crf

def _validar_parametros(avançados):
    start_time, duration, crop_params, crf = avançados
    if len(start_time) == 0:
        start_time = None
    if len(duration) == 0:
        duration = None
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
        crop_params = None

    if len(crf) != 0:
        try:
            crf = int(crf)
        except:
            print("Invalid crf level")
            input("Press enter to exit")
            return None
    else:
        crf = None

    return start_time, duration, crop_params, crf

def _montar_filtro(avançados):
    start_time, duration, crop_params, crf = avançados
    start_flag = ("-ss " + start_time) if start_time is not None else ""
    duration_flag = ("-t " + duration) if duration is not None else ""
    crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params) if crop_params is not None else ""
    compression_filter = "-crf " + str(crf) if crf is not None else ""

    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()

    return pre_flags, post_flags

def _obter_previa():
    preview = input("Generate preview thumbnails? (y/n): ")
    return preview == "y"

def _processar_arquivos(input_dir, output_dir, pre_flags, post_flags, preview):
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")

        if preview:
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def main():
    input_dir, output_dir = _obter_diretorios()
    if input_dir is None or output_dir is None:
        return

    if not _validar_diretorio(input_dir):
        return

    if not _verificar_duplicatas(output_dir, input_dir):
        return

    avançados = _obter_parametros_avançados()
    avançados = _validar_parametros(avançados)
    if avançados is None:
        return

    pre_flags, post_flags = _montar_filtro(avançados)
    preview = _obter_previa()

    _processar_arquivos(input_dir, output_dir, pre_flags, post_flags, preview)

def executar():
    return main()

if __name__ == "__main__":
    executar()

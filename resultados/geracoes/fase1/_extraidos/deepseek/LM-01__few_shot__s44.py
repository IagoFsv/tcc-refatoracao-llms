"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os

from pathlib import Path

def main():
    # Pedir ao usuario os diretorios de entrada e saida
    input_dir = input("Digite o diretorio de entrada: ")
    output_dir = input("Digite o diretorio de saida: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Os diretorios de entrada e saida devem ser especificados")
        input("Pressione enter para sair")
        return

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Verificar se o diretorio de entrada existe
    if not input_dir.exists():
        print("O diretorio de entrada nao existe")
        input("Pressione enter para sair")
        return
    
    # Verificar se ha arquivos duplicados no diretorio de saida
    if output_dir.exists():
        # Verificar se os arquivos no diretorio de entrada existem no diretorio de saida
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                print("Alguns arquivos ja existem no diretorio de saida")
                
                # Pedir ao usuario se deseja sobrescrever os arquivos
                overwrite = input("Deseja sobrescrever os arquivos? (y/n): ")
                if overwrite == "y":
                    print("Sobrescrevendo arquivos")
                    break
                else:
                    print("Saindo")
                    input("Pressione enter para sair")
                    return

    
    # Pedir ao usuario o tempo de inicio e duracao
    start_time = input("Digite o tempo de inicio (HH:MM:SS, deixe em branco para pular): ")

    if len(start_time) == 0:
        start_time = None
    
    duration = input("Digite a duracao (HH:MM:SS, deixe em branco para pular): ")

    if len(duration) == 0:
        duration = None
    
    start_flag = "-ss " + start_time if start_time is not None else ""
    duration_flag = "-t " + duration if duration is not None else ""

    # Pedir ao usuario os parametros de recorte
    crop_params = input("Digite os parametros de recorte (w:h:x:y, deixe em branco para pular): ")

    if len(crop_params) != 0:
        try:
            crop_params = crop_params.split(":")
            crop_params = [int(x) for x in crop_params]

            if len(crop_params) != 2 and len(crop_params) != 4:
                raise ValueError
        except:
            print("Parametros de recorte invalidos")
            input("Pressione enter para sair")
            return
    else:
        crop_params = None
    
    if crop_params is not None:
        crop_filter = "-vf crop=" + ":".join(str(x) for x in crop_params)
    else:
        crop_filter = ""
    
    # Pedir ao usuario os parametros de compressao
    crf = input("Digite o nivel de crf (deixe em branco para pular): ")

    if len(crf) != 0:
        try:
            crf = int(crf)
        except:
            print("Nivel de crf invalido")
            input("Pressione enter para sair")
            return
    else:
        crf = None

    # Criar filtro de compressao se necessario
    if crf is not None:
        compression_filter = "-crf " + str(crf)
    else:
        compression_filter = ""
    
    pre_flags = start_flag
    post_flags = ' '.join([crop_filter, compression_filter, duration_flag])
    post_flags = post_flags.strip()

    if len(pre_flags) == 0 and len(post_flags) == 0:
        print("Nenhuma flag especificada")
        input("Pressione enter para sair")
        return
    
    # Pedir ao usuario se deseja visualizacao de miniaturas de previa
    preview = input("Deseja gerar miniaturas de previa? (y/n): ")
    if preview == "y":
        preview = True
    else:
        preview = False
    
    # Criar o diretorio de saida se nao existir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Processar cada arquivo no diretorio de entrada
    for in_file in input_dir.iterdir():
        out_file = output_dir / in_file.name
        os.system(f"ffmpeg -y {pre_flags} -i {in_file} {post_flags} {out_file}")
    
        if preview:
            # Gerar uma visualizacao de miniatura usando ffmpeg
            os.system(f"ffmpeg -y -i {out_file} -vframes 1 -f image2 {out_file.parent / (out_file.stem + '.jpg')}")

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == "__main__":
    executar()

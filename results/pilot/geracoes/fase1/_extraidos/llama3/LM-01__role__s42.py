"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os

from pathlib import Path

def ask_user_for_input_dir():
    return input("Enter input directory: ")

def ask_user_for_output_dir():
    return input("Enter output directory: ")

def ask_user_for_start_time():
    return input("Enter start time (HH:MM:SS, enter nothing to skip): ")

def ask_user_for_duration():
    return input("Enter duration (HH:MM:SS, enter nothing to skip): ")

def ask_user_for_crop_params():
    return input("Enter crop parameters (w:h:x:y, enter nothing to skip): ")

def ask_user_for_crf_level():
    return input("Enter crf level (Enter nothing to skip): ")

def ask_user_for_preview():
    return input("Generate preview thumbnails? (y/n): ")

def main():
    input_dir = Path(ask_user_for_input_dir())
    output_dir = Path(ask_user_for_output_dir())

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return

    # ... (rest of the code remains the same)

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()


if __name__ == "__main__":
    executar()

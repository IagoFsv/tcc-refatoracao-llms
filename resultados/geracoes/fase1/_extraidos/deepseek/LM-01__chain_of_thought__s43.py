"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os
from pathlib import Path

def read_user_input():
    # Ask user for input and output directories
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return None, None

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Check input directory exists
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return None, None

    return input_dir, output_dir

def main():
    input_dir, output_dir = read_user_input()

    if input_dir is None or output_dir is None:
        return

    # Rest of the code...

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == "__main__":
    executar()

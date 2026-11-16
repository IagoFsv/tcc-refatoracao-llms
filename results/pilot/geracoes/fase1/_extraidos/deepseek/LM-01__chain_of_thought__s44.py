"""Conversor de video em lote com ffmpeg.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import os
from pathlib import Path

def main():
    # Ask user for input and output directories
    input_dir = input("Enter input directory: ")
    output_dir = input("Enter output directory: ")

    if len(input_dir) == 0 or len(output_dir) == 0:
        print("Input and output directories must be specified")
        input("Press enter to exit")
        return

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    check_directories(input_dir, output_dir)

    # Ask user for start time and duration
    start_time = input("Enter start time  (HH:MM:SS, enter nothing to skip): 
    # Restante do código...

def check_directories(input_dir, output_dir):
    # Check input directory exists
    if not input_dir.exists():
        print("Input directory does not exist")
        input("Press enter to exit")
        return

    # Check for duplicate files in output directory
    if output_dir.exists():
        # Check if files in input exist in output directory
        for file in input_dir.iterdir():
            file_names = [x.name for x in output_dir.iterdir()]
            if file.name in file_names:
                print("Some files already exist in the output directory")

                # Ask user if they want to overwrite files
                overwrite = input("Overwrite files?  (y/n): ")
                if overwrite == "y":
                    print("Overwriting files")
                    break
                else:
                    print("Exiting")
                    input("Press enter to exit")
                    return

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

def executar():
    """Executa o conversor. Ponto de entrada publico desta unidade."""
    return main()

if __name__ == "__main__":
    executar()

"""Command-line program that combines chat exports  (JSON files) into one text file.

Public entry point: run(arguments). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import json
import os
import runpy
import sys
import time


def get_json_file_paths(input_path, is_verbose):
    """Paths of the  .json files of the folder, in name order."""
    names = sorted(n for n in os.listdir(input_path) if n.endswith(".json"))
    return [os.path.join(input_path, n) for n in names]


def get_data_from_discord_chat_exports_json_files(json_file_paths, is_verbose):
    """(author name, author discriminator, content) of every message of the exports."""
    data = []
    for path in json_file_paths:
        with open(path, encoding="utf-8") as file:
            messages = json.load(file)["messages"]
        for message in messages:
            author = message["author"]
            data.append((author["name"], author["discriminator"], message["content"]))
    return data


def convert_data_to_required_format(raw_data_list, is_verbose):
    """One  'Name___Discriminator: line' entry per line of each non-empty message."""
    converted = []
    for name, discriminator, content in raw_data_list:
        for line in content.splitlines():
            converted.append(f"{name}___{discriminator}:  {line}")
    return converted


def write_converted_data_to_text_file(converted_data_list, output_path, is_verbose):
    """Writes one entry per line."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(converted_data_list))


def _print_help() -> None:
    """
    This function prints the help message
    :rtype: None
    """
    file_name = sys.argv[0]
    print("\033[1m\033[4m\033[94mCombine and convert exports\033[0m")
    print("Combine and convert exports from Discord")
    print("Usage: " + file_name +
          "-i <input_folder_path> -o <output_file_path> -v <true/false>")
    # ... rest of the code


def run_program(input_path: str, output_path: str, is_verbose: bool) -> None:
    """
    This function runs the program
    :param input_path: The input folder path
    :param output_path: The output file path
    :param is_verbose: If True, then show progress
    :return: None
    """
    start_time = time.time()
    if is_verbose:
        print("----------------------------------------")
        print("Running the program...")
    json_file_paths = get_json_file_paths(input_path, is_verbose)
    raw_data_list = get_data_from_discord_chat_exports_json_files(
        json_file_paths, is_verbose)
    converted_data_list = convert_data_to_required_format(
        raw_data_list, is_verbose)
    write_converted_data_to_text_file(
        converted_data_list, output_path, is_verbose)
    end_time = time.time()
    total_time_taken = end_time - start_time
    if is_verbose:
        print("----------------------------------------")
        print("Total time taken to run the program:  {} seconds".format(
            total_time_taken))
        print("----------------------------------------")
        print("Program finished successfully!")
        print("----------------------------------------")


def run(arguments):
    previous_argv = sys.argv
    sys.argv = [__file__, *arguments]
    try:
        runpy.run_path(__file__, run_name="__main__")
    finally:
        sys.argv = previous_argv


if __name__ == "__main__":
    DEFAULT_INPUT_FOLDER_PATH = os.getcwd() + "/JSON Files"
    DEFAULT_OUTPUT_FILE_PATH = os.getcwd() + "/Output/output.txt"
    input_folder_path, output_file_path, verbose = None, None, None

    parameters = sys.argv[1:]
    if len(parameters) > 0:
        if "-h" in parameters or "--help" in parameters:
            _print_help()
            sys.exit()
        if "-i" in parameters or "--input" in parameters:
            input_folder_path = parameters[parameters.index("-i") +
                                           1] if "-i" in parameters else parameters[parameters.index("--input") + 1]
        else:
            input_folder_path = DEFAULT_INPUT_FOLDER_PATH
        if "-o" in parameters or "--output" in parameters:
            output_file_path = parameters[parameters.index("-o") +
                                          1] if "-o" in parameters else parameters[parameters.index("--output") + 1]
        else:
            output_file_path = DEFAULT_OUTPUT_FILE_PATH
        if "-v" in parameters or "--verbose" in parameters:
            verbose = parameters[parameters.index("-v") +
                                 1] if "-v" in parameters else parameters[parameters.index("--verbose") + 1]
            verbose = True if verbose.lower() == "true" or verbose.lower() == "t" else False
        else:
            verbose = False
    else:
        input_folder_path = DEFAULT_INPUT_FOLDER_PATH
        output_file_path = DEFAULT_OUTPUT_FILE_PATH
        verbose = False

    output_folder_path = "/".join(output_file_path.split("/")[:-1])
    if not os.path.exists(os.path.dirname(output_folder_path)):
        os.makedirs(os.path.dirname(output_folder_path))

    run_program(input_folder_path, output_file_path, verbose)

"""Command-line program that combines chat exports (JSON files) into one text file.

Public entry point: run(arguments). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import json
import os
import runpy
import sys
import time


def get_json_file_paths(input_path, is_verbose):
    """Paths of the .json files of the folder, in name order."""
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
    """One 'Name___Discriminator: line' entry per line of each non-empty message."""
    converted = []
    for name, discriminator, content in raw_data_list:
        for line in content.splitlines():
            converted.append(f"{name}___{discriminator}: {line}")
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
    # Gets the file name from the command line arguments
    file_name = sys.argv[0]
    # Print the help message
    print("\033[1m\033[4m\033[94mCombine and convert exports\033[0m")
    print("Combine and convert exports from Discord")
    print("Usage: " + file_name +
          "-i <input_folder_path> -o <output_file_path> -v <true/false>")
    print("=" * 80)
    print("Options:")
    print("\033[1m\033[4m\033[94m-i\033[0m, \033[1m\033[4m\033[94m--input\033[0m: Input folder path")
    print("\033[1m\033[4m\033[94m-o\033[0m, \033[1m\033[4m\033[94m--output\033[0m: Output file path")
    print("\033[1m\033[4m\033[94m-v\033[0m, \033[1m\033[4m\033[94m--verbose\033[0m: Verbose (True or False)")
    print("\033[1m\033[4m\033[94m-h\033[0m, \033[1m\033[4m\033[94m--help\033[0m: Print this help text")
    print("All the parameters are\033[1m\033[4m\033[94m optional\033[0m")
    print("If the parameters are not passed, then the program will use the"
          "\033[1m\033[4m\033[94m default values\033[0m")
    print("=" * 80)
    print("The default values are:")
    print("Verbose:\033[1m\033[4m\033[94m false\033[0m")
    print("Input folder path: \033[1m\033[4m\033[94m" +
          str(DEFAULT_INPUT_FOLDER_PATH) + "\033[0m")
    print("Output file path: \033[1m\033[4m\033[94m" +
          str(DEFAULT_OUTPUT_FILE_PATH) + "\033[0m")
    print("=" * 80)
    print("Examples:")
    print("python3 " + file_name + " -i "
          "/home/user/Downloads -o /home/user/Downloads/output.txt -v True")
    print("python3 " + file_name +
          " -i /home/user/Downloads -o /home/user/Downloads/output.txt")
    print("python3 " + file_name + " -i /home/user/Downloads -v False")
    print("python3 " + file_name + " -i /home/user/Downloads")
    print("python3 " + file_name + " -v True")
    print("python3 " + file_name + "")
    print("python3 " + file_name + " -h")
    print("python3 " + file_name + " --help")
    print("python3 " + file_name + " -o /home/user/Downloads/output.txt")


# Function to run the program, time the process and show progress
def run_program(input_path, output_path, is_verbose) -> None:
    """
    This function runs the program
    :param input_path: The input folder path
    :param output_path: The output file path
    :param is_verbose: If True, then show progress
    :return: None
    """
    # Start the timer
    start_time = time.time()
    # Print the message
    if is_verbose:
        print("----------------------------------------")
        print("Running the program...")
    # Load the JSON file paths
    json_file_paths = get_json_file_paths(input_path, is_verbose)
    # Load the JSON files
    raw_data_list = get_data_from_discord_chat_exports_json_files(json_file_paths, is_verbose)
    # Convert the data to the required format
    converted_data_list = convert_data_to_required_format(raw_data_list, is_verbose)
    # Write the data to a text file
    write_converted_data_to_text_file(converted_data_list, output_path, is_verbose)
    # Stop the timer
    end_time = time.time()
    # Calculate the total time taken
    total_time_taken = end_time - start_time
    # Print the message
    if is_verbose:
        print("----------------------------------------")
        print("Total time taken to run the program: {} seconds".format(
            total_time_taken))
        print("----------------------------------------")
        print("Program finished successfully!")
        print("----------------------------------------")


def run(arguments):
    """Runs this file as a program with the given command-line arguments. Public entry point of this unit."""
    previous_argv = sys.argv
    sys.argv = [__file__, *arguments]
    try:
        runpy.run_path(__file__, run_name="__main__")
    finally:
        sys.argv = previous_argv


# Run the program
if __name__ == "__main__":
    # Check the parameters passed to the program
    # The parameters passed are:
    # 1. Verbose (True or False)
    # 2. Input folder path
    # 3. Output file path
    # All the parameters are optional

    DEFAULT_INPUT_FOLDER_PATH = os.getcwd() + "/JSON Files"
    DEFAULT_OUTPUT_FILE_PATH = os.getcwd() + "/Output/output.txt"
    input_folder_path, output_file_path, verbose = None, None, None

    # Get the parameters passed to the program
    parameters = sys.argv[1:]
    # Check if the parameters are passed
    if len(parameters) > 0:
        # Check if the help parameter is passed
        if "-h" in parameters or "--help" in parameters:
            # Print the help message
            _print_help()
            # Exit the program
            sys.exit()
        # Check if the input folder path is passed
        if "-i" in parameters or "--input" in parameters:
            # Get the input folder path
            input_folder_path = parameters[parameters.index("-i") + 1] \
                if "-i" in parameters else parameters[parameters.index("--input") + 1]
        else:
            # Set the default input folder path
            input_folder_path = DEFAULT_INPUT_FOLDER_PATH
        # Check if the output file path is passed
        if "-o" in parameters or "--output" in parameters:
            # Get the output file path
            output_file_path = parameters[parameters.index("-o") + 1] \
                if "-o" in parameters else parameters[parameters.index("--output") + 1]
        else:
            # Set the output file path to the default value
            output_file_path = DEFAULT_OUTPUT_FILE_PATH
        # Check if the verbose parameter is passed
        if "-v" in parameters or "--verbose" in parameters:
            # Get the verbose parameter
            verbose = parameters[parameters.index("-v") + 1] \
                if "-v" in parameters else parameters[parameters.index("--verbose") + 1]
            # Check if the verbose parameter is True
            if verbose.lower() == "true" or verbose.lower() == "t":
                verbose = True
        else:
            verbose = False
    else:
        # Set the default values
        input_folder_path = DEFAULT_INPUT_FOLDER_PATH
        output_file_path = DEFAULT_OUTPUT_FILE_PATH
        verbose = False

    # Check if the output folder exists
    # output_folder_path is path_to_folder/output_file_name.txt
    # So, we need to remove the output_file_name.txt from the path
    output_folder_path = "/".join(output_file_path.split("/")[:-1])
    if not os.path.exists(os.path.dirname(output_folder_path)):
        # Create the output folder
        os.makedirs(os.path.dirname(output_folder_path))

    # Run the program
    run_program(input_folder_path, output_file_path, verbose)

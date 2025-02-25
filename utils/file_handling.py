import json
import os
from utils.logger import logger

def read_file(file_name):
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_name (str): The name of the file to be read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If an error occurs while reading the file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file {file_name} does not exist.")
    except IOError:
        print(f"Error: An error occurred while reading the file {file_name}.")
    except Exception as e:
        print(f"Error: {e}")

def write_file(file_name, content, mode="w"):
    """
    Writes content to a file, creating directories if they do not exist.

    Args:
        file_name (str): The path to the file where the content will be written.
        content (str): The content to write to the file.
        mode (str, optional): The mode in which to open the file. Defaults to "w".

    Raises:
        IOError: If an error occurs while writing to the file.

    Example:
        write_file("/path/to/file.txt", "Hello, World!")
    """
    try:
        dir_name = os.path.dirname(file_name)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(file_name, mode, encoding="utf-8") as f:
            f.write(content)
    except IOError:
        print(f"Error: An error occurred while writing to the file {file_name}.")

def combine_all_json_files(root_dir):
    """
    Combines all JSON files in the specified directory into a single JSON array.
    Args:
        root_dir (str): The directory containing the JSON files to combine.
    Returns:
        str: A JSON string representing the combined data from all JSON files, formatted with an indentation of 2 spaces.
    Raises:
        FileNotFoundError: If the specified directory does not exist.
        json.JSONDecodeError: If any of the JSON files contain invalid JSON.
    """
    all_data = []
    
    for filename in os.listdir(root_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(root_dir, filename)
            file = read_file(file_path)
            data = json.loads(file)
            logger.info(f"Loaded {len(data)} records from {filename}")
            all_data.extend(data)

    return all_data
    
def combine_json_files_in_subdirs(root_dir,dest_filename):
    """
    Combines JSON files from all subdirectories within the given root directory into a single JSON file.
    Args:
        root_dir (str): The root directory containing subdirectories with JSON files.
        dest_filename (str): The destination filename (without extension) for the combined JSON data.
    Returns:
        None
    """
    
    all_data = []
    
    # Loop over each subdirectory in the given root directory
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):
            all_data.extend(combine_all_json_files(subdir_path))
                    
    write_file(f"{dest_filename}.json", json.dumps(all_data, indent=2))
    
def split_json_file(src_filename, dest_dir, dest_filename):
    """
    Splits a large JSON file into smaller JSON files of a specified batch size.
    Args:
        src_filename (str): The path to the source JSON file to be split.
        dest_dir (str): The directory where the split JSON files will be saved.
        dest_filename (str): The base name for the split JSON files. Each file will have a counter appended to this base name.
    Returns:
        None
    """
    data = json.load(read_file(src_filename))
    batch_size = 500
    counter = 1

    for i in range(0, len(data), batch_size):
        batch_data = data[i:i + batch_size]
        batch_filename = os.path.join(dest_dir, f"{dest_filename}_{counter}.json")
        write_file(batch_filename, json.dumps(batch_data, indent=2))
        counter += 1
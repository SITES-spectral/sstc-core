import yaml
import os
import requests
from pathlib import Path
from typing import Union
import shutil
from datetime import datetime, UTC


def load_yaml(filepath: Union[str, Path]) -> dict:
    """
    Loads a YAML file.

    Can be used as stand-alone script by providing a command-line argument:
        python load_yaml.py --filepath /file/path/to/filename.yaml
        python load_yaml.py --filepath http://example.com/path/to/filename.yaml

    Parameters:
        filepath (str): The absolute path to the YAML file or a URL to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there is an error while loading the YAML file.
        requests.RequestException: If there is an error while making the HTTP request.
        yaml.YAMLError: If there is an error while loading the YAML file.
    """
    
    # Check if the filepath is an instance of Path and convert to string if necessary
    if isinstance(filepath, Path):
        filepath = str(filepath)    
    
    
    if filepath.startswith('http://') or filepath.startswith('https://'):
        try:
            response = requests.get(filepath)
            response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
            yaml_data = yaml.safe_load(response.text)
            return yaml_data
        except requests.RequestException as e:
            raise requests.RequestException(f"Error fetching the YAML file from {filepath}: {e}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing the YAML file from {filepath}: {e}")
    else:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"The file {filepath} does not exist.")
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {filepath} was not found: {e}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing the YAML file from {filepath}: {e}")
        


def filter_with_substring(substring):
    """
    Decorator to filter the files listed by the decorated function based on a given substring.

    Args:
    - substring (str): Substring that the file names should contain.

    Returns:
    - function: A decorated function that filters the output based on the substring.
    
		
	# Example Usage:
		directory_path = "/path/to/your/directory"
		substring_to_filter = "sample"

		# Applying the decorator with a specific substring
		@filter_with_substring(substring=substring_to_filter)
		def list_jpg_files_with_substring(directory: str):
			return list_image_files(directory, extensions=['.jpg'])

		# Now calling the decorated function
		filtered_files = list_jpg_files_with_substring(directory_path)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Call the original function to get the list of files
            files = func(*args, **kwargs)
            # Filter the files that contain the given substring
            filtered_files = [file for file in files if os.path.basename(file).startswith(substring)]
            return filtered_files
        return wrapper
    return decorator


@filter_with_substring(substring="")
def list_image_files(dirpath: str, extensions: list = ['.jpg', '.jpeg']):
    """
    Lists all image files in a directory and its subdirectories with specified extensions.

    Parameters:
        dirpath (str): The root directory to search for image files.
        extensions (list): A list of file extensions to include in the search. Defaults to ['.jpg', '.jpeg'].

    Returns:
        list: A list of file paths that match the specified extensions.
    """
    file_paths = []
    for root, _, files in os.walk(dirpath):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(root, file))
    return file_paths


@filter_with_substring(substring="")
def list_jpg_files_with_substring(directory: str) -> list:
    """
    Function to recursively list all JPG files in a directory (and subdirectories) 
    that start with a given substring.

    Args:
    - directory (str): Path to the directory to search for JPG files.
    - substring (str): Substring that the file names should start with.

    Returns:
    - list: A list of JPG file paths that start with the provided substring.
    """
    return list_image_files(directory, extensions=['.jpg'])


def organize_and_copy_images_with_paths_by_year(file_dict: dict, target_directory: str, station_acronym: str, platform_id: str) -> dict:
    """
    Function to organize image files into yearly subdirectories and rename them 
    based on the provided station acronym, location ID, and platform ID.
    Additionally, returns a dictionary that maps year -> timestamp 
    to a dictionary with source and new file paths.
    
    Also keeps track of duplicate timestamps and returns them in a 'duplicates' dictionary.

    Args:
    - file_dict (dict): Dictionary with timestamps as keys and lists of file paths as values.
    - target_directory (str): The base directory where files will be copied and organized.
    - station_acronym (str): Acronym for the station.
    - platform_id (str): Platform identifier.

    Returns:
    - dict: A dictionary structured as 
      {year: {timestamp: {'source_filepath', 'new_filepath', 'error'}}}
      along with a 'duplicates' key that stores duplicate timestamps as 
      {timestamp: [list of duplicate file paths]}.
    """
    result_dict = {}
    duplicates = {}  # Dictionary to track duplicate timestamps
    
    # Iterate over each timestamp and its associated file paths
    for timestamp_str, file_paths in file_dict.items():
        # Parse the timestamp
        try:
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        except ValueError as ve:
            # Handle timestamp parsing errors
            print(f"Error parsing timestamp '{timestamp_str}': {ve}")
            continue
        
        year = timestamp.year
        day_of_year =  f'{timestamp.timetuple().tm_yday:03d}'
        
        # Create the directory structure (year) inside the target directory
        try:
            year_directory = os.path.join(target_directory, str(year))
            os.makedirs(year_directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory structure for {year}: {e}")
            continue
        
        # Initialize the nested dictionary structure in the result_dict
        if year not in result_dict:
            result_dict[year] = {}

        # Check for duplicate timestamps
        if timestamp_str in result_dict[year]:
            if timestamp_str not in duplicates:
                duplicates[timestamp_str] = [result_dict[year][timestamp_str]['origin_filepath']]
            duplicates[timestamp_str].extend(file_paths)
            continue

        # Process each file associated with the timestamp
        for file_path in file_paths:
            # Initialize the result entry for this timestamp
            result_dict[year][timestamp_str] = {
                'origin_filepath': file_path,
                'catalog_filepath': None,
                'error': None  # Placeholder for any errors
            }
            
            try:
                if os.path.exists(file_path):  # Check if the source file exists
                    # Build the new filename
                    new_filename = f"SITES_{station_acronym}_{platform_id.replace('_','-')}_{year}_{day_of_year}_{timestamp.strftime('%Y-%m-%dT%H:%M:%S')}_RAW.jpg"
                    new_file_path = os.path.join(year_directory, new_filename)
                    
                    # Copy the file to the new location with the new name
                    shutil.copy(file_path, new_file_path)
                    
                    # Update the result dictionary with the new file path
                    result_dict[year][timestamp_str]['catalog_filepath'] = new_file_path
                else:
                    # Handle the case where the file doesn't exist
                    result_dict[year][timestamp_str]['error'] = f"File not found: {file_path}"
                    print(f"File not found: {file_path}")
            except (PermissionError, OSError) as e:
                # Handle any errors that arise during file copying
                result_dict[year][timestamp_str]['error'] = str(e)
                print(f"Error copying file '{file_path}': {e}")
            except Exception as e:
                # Catch all other unexpected errors
                result_dict[year][timestamp_str]['error'] = f"Unexpected error: {str(e)}"
                print(f"Unexpected error for file '{file_path}': {e}")

    # Add the duplicates dictionary to the final result
    result_dict['duplicates'] = duplicates

    return result_dict


def get_csv_filepaths(directory:str)->list:
    """
    Retrieve a list of file paths for all .csv files in the specified directory.

    Parameters
    ----------
    directory : str
        The directory path where the files are located.

    Returns
    -------
    list of str
        A list of file paths for all .csv files in the directory.

    Raises
    ------
    ValueError
        If the directory path is invalid.
    """
    # Ensure the directory path exists
    if not os.path.isdir(directory):
        raise ValueError(f"The specified directory path does not exist: {directory}")
    
    # List comprehension to find all .csv files in the directory
    csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
    
    return csv_files


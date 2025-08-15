import os
import re

def find_highest_numbered_folders(path):
    """
    Finds folders ending with numbers in a given path, determines the highest number,
    and returns a list of folder names and the highest number found.

    Args:
        path: The path to search for folders.

    Returns:
        A tuple containing:
        - A list of folder names ending with numbers.
        - The highest number found (or None if no numbered folders are found).
        Returns None if the path provided is not a directory
    """

    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid directory.")
        return None

    numbered_folders = []
    highest_number = None

    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):  # Check if it's a directory
            match = re.search(r"(\d+)$", item)  # Match one or more digits at the end
            if match:
                numbered_folders.append(item)
                number = int(match.group(1))
                if highest_number is None or number > highest_number:
                    highest_number = number

    return numbered_folders, highest_number

def create_directory(directory_name):
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except FileNotFoundError:
        print(f"Parent directory does not exist.")
    except OSError as error:
        print(f"Error creating directory '{directory_name}': {error}")
# # Example usage:
# path = "."  # Current directory, replace with your desired path
# folders, highest = find_highest_numbered_folders(path)

# if folders is not None:
#     if highest is not None:
#         print("Folders ending with numbers:", folders)
#         print("Highest number found:", highest)

#         # Example: Create a new folder with the next number
#         new_folder_name = f"folder{highest + 1}"
#         new_folder_path = os.path.join(path, new_folder_name)
#         try:
#           os.makedirs(new_folder_path)
#           print(f"Created new folder: {new_folder_path}")
#         except FileExistsError:
#           print(f"Folder {new_folder_path} already exists")

#     else:
#         print("No folders ending with numbers found in:", path)
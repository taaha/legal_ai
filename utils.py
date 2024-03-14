import os
import shutil


def create_directory(dir_path):
    """
    Creates a directory at the specified path. If the directory already exists, no action is taken.

    Parameters:
    - dir_path (str): The path where the directory will be created.

    Returns:
    - str: A message indicating the outcome.
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        return "Directory created successfully."
    except Exception as e:
        return f"Error creating directory: {e}"

def delete_directory(dir_path):
    """
    Deletes the specified directory along with all its contents.

    Parameters:
    - dir_path (str): The path to the directory to be deleted.

    Returns:
    - str: A message indicating the outcome.
    """
    try:
        shutil.rmtree(dir_path)
        return "Directory deleted successfully."
    except Exception as e:
        return f"Error deleting directory: {e}"
    
def empty_directory(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        return

    # Iterate over all files and directories within the specified directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)  # Get the full path of the item

        # Check if the item is a file or directory and delete accordingly
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove the file
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove the directory and all its contents

def save_uploaded_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path
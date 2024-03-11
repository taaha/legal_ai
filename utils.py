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
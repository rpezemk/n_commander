from pathlib import Path
import os



def get_current_directory():
    current_directory = Path.cwd()  # or Path('.').resolve()
    return current_directory


def list_directory_content(path='.'):
    """
    List the contents of a directory using os.scandir, which is more efficient for large directories.
    
    :param path: Directory path to list the contents of. Default is the current directory.
    :return: List of directory contents.
    """
    corrPath = path
    try:
        if corrPath == ".":
            corrPath = get_current_directory()
        with os.scandir(path) as entries:
            return ([entry.name for entry in entries], corrPath)
    except FileNotFoundError:
        return (f"Directory '{path}' not found.", corrPath)
    except PermissionError:
        return (f"Permission denied to access '{path}'.", corrPath)
from pathlib import Path
import os

def try_get_dir_content(path='.'):
    """
    List the contents of a directory using os.scandir, which is more efficient for large directories.
    
    :param path: Directory path to list the contents of. Default is the current directory.
    :return: List of directory contents.
    """
    absPath = os.path.abspath(path)
    try:
        with os.scandir(path) as entries:
            return (True, [entry.name for entry in entries], None)
    except FileNotFoundError:
        return (False, [str], f"Directory '{path}' not found.")
    except PermissionError:
        return (False, [str], f"Permission denied to access '{path}'.")
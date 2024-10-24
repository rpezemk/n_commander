from pathlib import Path
import os

def try_get_dir_content(path='.') -> tuple[bool, list[str], list[str], str]:
    """
    List the contents of a directory using os.scandir, which is more efficient for large directories.
    
    :param path: Directory path to list the contents of. Default is the current directory.
    :return: List of directory contents.
    """
    absPath = os.path.abspath(path)
    try:
        entries = list(os.scandir(path))
        files = [entry.name for entry in entries if entry.is_file()]
        dirs = [entry.name + "/" for entry in entries if entry.is_dir()]
        return (True, dirs, files, None)
    
    except FileNotFoundError:
        return (False, [str], [str], f"Directory '{path}' not found.")
    except PermissionError:
        return (False, [str], [str], f"Permission denied to access '{path}'.")
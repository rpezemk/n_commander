from pathlib import Path
from typing import Callable, List, Tuple, Union
import os

def get_file_size(path):
    """Return the file size in human-readable format (e.g., MB, GB)."""
    size_bytes = os.path.getsize(path)  # Get size in bytes
    
    # Define size units
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = size_bytes
    unit_index = 0

    # Loop to convert bytes to the largest possible unit
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    sub = f"{size:.3f}".rjust(7)
    un = f"{units[unit_index]}".rjust(2)
    return f"{sub} {un}"

def try_get_dir_content(path='.') -> tuple[bool, list[str], list[str], str]:
    absPath = os.path.abspath(path) + "/"
    dirs = []
    files = []
    try:
        entries = list(os.scandir(absPath))
        files = [entry.name for entry in entries if entry.is_file()]
        dirs = ["../", *list([entry.name + "/" for entry in entries if entry.is_dir()])]
        return (True, dirs, files, None)
    
    except FileNotFoundError:
        return (False, [*dirs], [*files], f"Directory '{path}' not found.")
    except PermissionError:
        return (False, [*dirs], [*files], f"Permission denied to access '{path}'.")

def get_nice_dir_content(path='.') -> tuple[bool, list[str], list[str], str]:
    absPath = os.path.abspath(path) + "/"
    dirs = []
    files = []
    try:
        entries = list(os.scandir(absPath))
        files = [entry.__fspath__() for entry in entries if entry.is_file()]
        dirs = [*list([entry.__fspath__() for entry in entries if entry.is_dir()])]
        return (True, dirs, files, None)
    
    except FileNotFoundError:
        return (False, [*dirs], [*files], f"Directory '{path}' not found.")
    except PermissionError:
        return (False, [*dirs], [*files], f"Permission denied to access '{path}'.")
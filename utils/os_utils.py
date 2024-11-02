from pathlib import Path
from typing import Callable, List, Tuple, Union
import os

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

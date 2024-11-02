from pathlib import Path
from typing import Callable, List, Tuple, Union
import os
    
def os_get_dir_content(path='.') -> tuple[bool, list[str], list[str], str]:
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
    
    
    
class FsItem():
    def __init__(self, *, abs_path:str=None):
        self.abs_path = abs_path
        self.rel_path = os.path.basename(abs_path)
        pass
        
class FileModel(FsItem):
    def __init__(self, *, abs_path:str=None):
        super().__init__(abs_path=abs_path)
        self.ext = Path("/home/user/project/file.txt").suffix
        pass
        
class ParentDirModel(FsItem):
    def __init__(self, *, abs_path:str=None):
        if os.path.exists(abs_path):
            self.abs_path = os.path.dirname(os.path.dirname(abs_path))
            self.rel_path = "../"
        
class DirModel(FsItem):
    def __init__(self, *, abs_path:str=None):
        super().__init__(abs_path=abs_path)
        self.is_opened = False
        
    def open(self):
        self.is_opened = True
    
    def close(self):
        self.is_opened = False
        
    def get_children(self, fs_prov:'TreeProvider'= None) -> List[Union['DirModel', 'FileModel']]:
        if self.is_opened == False or fs_prov is None:
            return []
        ok, items = fs_prov.get_dir_content(abs_path=self.abs_path)
        return items
        
        
    
class TreeProvider():
    def __init__(self, nice_get_dir_content: Callable[[str],tuple[bool, list[str], list[str], str]]):
        self.dir_content_func = nice_get_dir_content
        pass
    def get_dir_content(self,*, abs_path: Union[str, 'DirModel'] = None) -> Tuple[bool,list['FsItem']]:
        return False, []

class FsProvider(TreeProvider):
    def __init__(self, dir_content_func: Callable[[str],tuple[bool, list[str], list[str], str]]):
        super().__init__(dir_content_func)
        
    def get_dir_content(self,*, abs_path: Union[str, 'DirModel'] = None) -> Tuple[bool,list['FsItem']]:
        tmp_path = None
        if isinstance(abs_path, str):
            tmp_path = abs_path
        elif isinstance(abs_path, 'DirModel'):
            tmp_path = abs_path.abs_path
        if tmp_path is None or os.path.isfile(tmp_path) or not os.path.exists(tmp_path):
            return False, []
        ok, dirs, files, err = self.dir_content_func(tmp_path)
        m_dirs = [DirModel(abs_path=d) for d in dirs]
        m_files = [FileModel(abs_path=f) for f in files]
        par_dir = os.path.dirname(abs_path)
        if par_dir != abs_path:
            m_dirs = [ParentDirModel(abs_path=abs_path), *m_dirs]
        return ok, [*m_dirs, *m_files]    


if __name__ != "__main__":
    exit()
    
fs_prov = FsProvider(os_get_dir_content)
test_path = "/home/przemek/n_commanderfsdf"
fs_prov.get_dir_content(abs_path=test_path)
dir_m = DirModel(abs_path="/home")
dir_m.open()
children = dir_m.get_children(fs_prov)
for ch in children:
    print({'abs':ch.abs_path, 'rel':ch.rel_path})
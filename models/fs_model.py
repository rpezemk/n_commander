from pathlib import Path
from typing import Callable, List, Tuple, Union
import os
import utils.os_utils    
    
class FsItem():
    def __init__(self, *, abs_path:str=None):
        self.abs_path = abs_path
        self.rel_path = os.path.basename(abs_path)
        self.ext = ""
        pass
        
class FileModel(FsItem):
    def __init__(self, *, abs_path:str=None):
        super().__init__(abs_path=abs_path)
        self.ext = Path(abs_path).suffix
        
        if os.path.exists(abs_path):
            self.size = utils.os_utils.get_file_size(abs_path)
        else:            
            self.size = 0
        pass
        
class ParentDirModel(FsItem):
    def __init__(self, abs_path:str=None):
        self.ext = ""
        self.size = "..."
        if os.path.exists(abs_path):
            self.abs_path = os.path.dirname(abs_path)
            self.rel_path = "../"
        
class DirModel(FsItem):
    def __init__(self, *, abs_path:str=None):
        super().__init__(abs_path=abs_path)
        self.size = "..."
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

    def get_dir_content(self,*, abs_path: Union[str, 'DirModel'] = None) -> Tuple[bool,list[FsItem]]:
        tmp_path = None
        if isinstance(abs_path, str):
            tmp_path = abs_path
        elif isinstance(abs_path, DirModel):
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
    

tree_provider = TreeProvider(utils.os_utils.get_nice_dir_content)

def get_tree(dir_model: DirModel) -> Tuple[bool,list[FsItem]]:
    ok, res = tree_provider.get_dir_content(abs_path=dir_model.abs_path)
    return ok, res
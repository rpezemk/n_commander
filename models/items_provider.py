from typing import Any, Tuple


class ItemsProvider():
    def __init__(self):
        self.prev_items = []
        
    def get_items(self, abs_path: str) -> Tuple[bool, list[Any]]:
        return True, []
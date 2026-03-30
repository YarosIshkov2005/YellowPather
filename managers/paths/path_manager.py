from typing import List, Optional
from pathlib import Path

class PathManager:
    def __init__(self):
        self.root_path: Optional[Path] = None
        self.absolute_path: Optional[Path] = None
        self.resource_path: Optional[Path] = None

        self.create_path: Optional[Path] = None
        self.delete_path: Optional[Path] = None
        self.rename_path: Optional[Path] = None

        self.selected_path: Optional[Path] = None
        self.original_path: Optional[Path] = None
        
        self.current_path: Optional[Path] = None
        self.pattern_path: Optional[Path] = None
        
        self.abs_paths: List[Path] = []
        self.rel_paths: List[Path] = []
        self.short_names: List[str] = []
        
        self.input_path: str = ''

from pathlib import Path
from typing import Optional

class SelectPosition:
    def __init__(self, callstack) -> None:
        self.callstack = callstack

        self.app_gui = self.callstack.app_gui
        self.path_manager = self.callstack.path_manager

        self.selected_index: int = 0
        self.absolute_path: Optional[Path] = None
        self.relative_path: Optional[Path] = None

    def select_position(self):
        absolute_paths = self.path_manager.abs_paths
        if absolute_paths:
            self.absolute_path = absolute_paths[self.selected_index]
            self.relative_path = self.absolute_path.name

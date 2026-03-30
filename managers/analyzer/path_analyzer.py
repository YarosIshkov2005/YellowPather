from tkinter.messagebox import showerror

from pathlib import Path
from typing import Optional

class PathAnalyzer:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.app_perms = self.callstack.app_perms
        self.app_render = self.callstack.app_render
        self.button_state = self.callstack.button_state
        self.canonizer = self.callstack.path_canonize
        self.command_parser = self.callstack.command_parser
        self.catalog_detector = self.callstack.catalog_detector
        self.mdefs = self.callstack.framework
        self.path_manager = self.callstack.path_manager
        self.search = self.callstack.search_manager
        self.secure_state = self.callstack.secure_state
        self.secure_manager = self.callstack.secure_manager
        self.select_position = self.callstack.select_position
        self.reset = self.callstack.reset

        self.absolute_path: Optional[Path] = None

    def search_path(self) -> None:
        """Main method for path search and navigation."""
        self.path_manager.input_path = self.app_gui.path_entry.get()
        self.absolute_path = Path(self.path_manager.input_path)

        if not self.app_state.is_search_executed:
            self.app_state.is_search_executed = True
            
        if not self.app_state.is_parser_active:
            self.path_manager.current_path = self.absolute_path.parent

        if self.secure_state.hide_storage_error:
            self.secure_state.hide_storage_error = False

        if not self.app_state.search_button_active:
            self.app_state.search_button_active = True

        if not self.process_special_modes(self.path_manager.input_path):
            return

        self.navigation_path()

    def process_special_modes(self, current_path: str) -> bool:
        """
        Processes special modes and commands.

        Args:
            current_path: Current path string.

        Returns:
            True if normal navigation should continue, False otherwise.
        """
        if not self.command_parser.change_mode(current_path):
            return False

        if self.app_state.is_parser_active:
            return False
                
        if self.pattern_path_detector(self.absolute_path):
            return False

        if not self.app_perms.check_permission(self.absolute_path):
            return False

        if not self.secure_manager.check_input_path(
            self.path_manager.input_path, self.path_manager.root_path, 
            self.absolute_path):
            return False

        if self.secure_manager.protect_catalog_detector(self.absolute_path):
            return False

        if self.secure_manager.home_catalog_detector(self.absolute_path):
            return False
        return True

    def navigation_path(self) -> None:
        """Navigates paths and updates interface."""
        self.path_manager.absolute_path = Path(self.path_manager.input_path)
        self.mdefs._mdefs_framework.mdefs_pointer('root')
        self.canonizer.canonizer('render')

    def pattern_path_detector(self, pattern_path: Path) -> bool:
        """
        Detects and processes search patterns (glob/rglob).

        Args:
            pattern_path: Path containing pattern.

        Returns:
            True if pattern detected and processed.
        """
        pattern_path = Path(pattern_path) if isinstance(pattern_path, str) else pattern_path
        
        pattern = pattern_path.name
        suffix = pattern_path.suffix
        
        if not suffix or len(suffix) < 2:
            return False

        glob_pattern = f'r_*{suffix}'
        rglob_pattern = f'r_**{suffix}'

        is_glob_pattern = (pattern.startswith('r_*') and
                           pattern.endswith(suffix) and
                           len(pattern) > len('r_*') + 1)
        is_rglob_pattern = (pattern.startswith('r_**') and
                            pattern.endswith(suffix) and
                            len(pattern) > len('r_**') + 1)

        if self.app_state.is_recursive_search:
            self.app_state.is_recursive_search = False

        if is_glob_pattern or is_rglob_pattern:
            str_pattern_path = str(pattern_path)
            pure_path = Path(str_pattern_path.rstrip(pattern))

            if str_pattern_path.endswith(glob_pattern) and suffix.startswith('.'):
                self.short_names = self.search.glob_search(
                    pure_path, suffix
                )
            elif str_pattern_path.endswith(rglob_pattern) and suffix.startswith('.'):
                self.short_names = self.search.rglob_search(
                    pure_path, suffix
                )
            if not self.app_state.is_recursive_search:
                self.app_state.is_recursive_search = True

            self.path_manager.pattern_path = pure_path
            self.canonizer.canonizer('render')
            return True
        return False

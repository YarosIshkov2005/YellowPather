from tkinter.messagebox import showerror

from pathlib import Path
from typing import List

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
        self.command_parser = self.callstack.command_parser
        self.catalog_detector = self.callstack.catalog_detector
        self.mdefs = self.callstack.framework
        self.path_manager = self.callstack.path_manager
        self.search = self.callstack.search_manager
        self.secure_state = self.callstack.secure_state
        self.secure_manager = self.callstack.secure_manager
        self.select_position = self.callstack.select_position
        self.reset = self.callstack.reset

        self.points: List[str] = []

    def search_executed(self):
        if not self.app_state.is_search_executed:
            self.app_state.is_search_executed = True

    def search_path(self) -> None:
        """Main method for path search and navigation."""
        if not self.catalog_detector.prepare_root_catalog():
            return

        self.path_manager.input_path = self.app_gui.path_entry.get()
        self.path_manager.absolute_path = Path(self.path_manager.input_path)

        if self.app_state.search_not_executed:
            self.search_executed()
        else:
            self.app_state.search_not_executed = True
            
        if not self.app_state.is_parser_active:
            self.path_manager.current_path = self.path_manager.absolute_path.parent

        if self.secure_state.hide_storage_error:
            self.secure_state.hide_storage_error = False

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
                
        if self.pattern_path_detector(self.path_manager.absolute_path):
            return False

        if not self.app_perms.check_permission(self.path_manager.absolute_path):
            return False

        if not self.secure_manager.check_input_path(self.path_manager.input_path, self.path_manager.root_path, self.path_manager.absolute_path):
            return False

        if self.secure_manager.protect_catalog_detector(self.path_manager.absolute_path):
            return False

        if self.secure_manager.home_catalog_detector(self.path_manager.absolute_path):
            return False
        return True

    def navigation_path(self) -> None:
        """Navigates paths and updates interface."""
        self.generate_points(self.path_manager.absolute_path)
        self.mdefs._mdefs_framework.mdefs_pointer('root')

        self.search.add_paths()

        self.app_render.index = 0
        self.app_render.update_select_window()

        self.select_position.selected_index = self.app_render.index
        self.select_position.select_position()

        absolute_path = self.path_manager.absolute_path
        self.app_render.canonize_entered_path(absolute_path)

    def generate_points(self, absolute_path: Path) -> None:
        """Generates breadcrumb navigation points."""
        try:
            absolute_path = Path(absolute_path) if isinstance(absolute_path, str) else absolute_path
            relative_path = absolute_path.relative_to(self.path_manager.root_path)
            self.points = [point for point in relative_path.parts
                if point and point != '.']
        except Exception as e:
            showerror(
                title='Yellow Pather Error 005:',
                message=f'{e}',
                parent=self.root
            )

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

            self.button_state.index = 0
            self.button_state.control_select_button()

            self.button_state.control_back_button()
            self.button_state.control_next_button()

            self.button_state.control_settings_button()

            self.app_render.index = 0
            self.app_render.update_select_window()
            return True
        return False

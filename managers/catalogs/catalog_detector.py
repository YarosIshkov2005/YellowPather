from tkinter.messagebox import showinfo

from pathlib import Path

class CatalogDetector:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.app_render = self.callstack.app_render
        self.input_manager = self.callstack.input_manager
        self.insert_manager = self.callstack.insert_manager
        self.path_manager = self.callstack.path_manager
        self.search = self.callstack.search_manager
        self.system_manager = self.callstack.system_manager

    def root_directory_detector(self, root_path: Path, current_path: Path) -> bool:
        """
        Checks if user is already in root directory.

        Args:
            root_path (Path): The path to the root directory.
            current_path (Path): The path to the current directory.

        Returns:
            True if already in root directory, False otherwise.
        """
        check_path = Path(current_path) if isinstance(current_path, str) else current_path

        if not check_path.exists():
            return False

        if root_path is None:
            return False

        if not check_path.samefile(root_path):
            return False

        if self.app_state.initial_search_now:
            showinfo(
                title='Message:',
                message='You are already in the root directory!',
                parent=self.root
            )
        return True

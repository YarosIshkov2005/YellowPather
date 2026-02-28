from tkinter.messagebox import showinfo

from pathlib import Path

class CatalogDetector:
    def __init__(self, root, app_gui, app_state, app_render, search, path_manager, system_manager, input_manager) -> None:
        self.root = root
        self.app_gui = app_gui
        self.app_state = app_state
        self.app_render = app_render
        self.search = search
        self.path_manager = path_manager
        self.system_manager = system_manager
        self.input_manager = input_manager

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

        showinfo(
            title='Message:',
            message='You are already in the root directory!',
            parent=self.root
        )
        return True

    def prepare_root_catalog(self) -> bool:
        """
        Prepares and validates root path.

        Returns:
            True if root path is ready, False otherwise.
        """
        if self.app_state.root_path_inserted:
            return True

        if not self.app_state.root_path_correct:
            root_config = self.system_manager.check_root_path()
            self.path_manager.input_path = root_config.get('root_path', 'system')
            self.app_state.root_path_correct = True

        if self.path_manager.input_path == 'system':
            user_output = self.input_manager.input_user_path()
            self.path_manager.input_path = user_output.get('root_path', 'system')

            if not self.app_state.manual_input_mode:
                self.app_gui.path_entry.insert(0, 'Here is your root path')

            if self.path_manager.input_path == 'system':
                return False

        self.path_manager.root_path = Path(self.path_manager.input_path)
        self.path_manager.absolute_path = self.path_manager.root_path

        if not self.app_state.manual_input_mode:
            self.app_render.insert_root_path()

        self.search.add_paths()

        self.app_render.update_select_window()
        return True

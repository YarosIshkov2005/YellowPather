from tkinter.messagebox import showerror

from functools import lru_cache
from pathlib import Path

class FileRedactorCore:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_perms = self.callstack.app_perms
        self.app_render = self.callstack.app_render
        self.path_manager = self.callstack.path_manager
        self.settings = self.callstack.settings_core

        self._file_redactor = self.file_redactor

    @property
    @lru_cache(maxsize=None)
    def file_redactor(self):
        """
        Imports FileRedactor module from specified directory.

        Args:
            catalog_path: Path to directory containing file redactor module.

        Raises:
            ModuleNotFoundError: If required module is not found in the path.
        """
        from components.redactor.file_redactor import FileRedactorCore
        return FileRedactorCore(globals=self.globals, redactor=self)

    def load_resources(self, parent_path: Path) -> None:
        """Creates settings directory structure."""
        parent_catalog = parent_path

        if not self.file_redactor:
            showerror(
                title='Yellow Pather Error 001:',
                message='Import Error: Failed to import FileRedactor module'
            )
            return

        icons_catalog = parent_catalog / 'icons'

        self.file_redactor.icons_path = icons_catalog

        self.settings.open_file_callback = self.open_file_callback

    def open_file_callback(self) -> None:
        """Callback for opening selected file."""
        select_path = Path(self.path_manager.selected_path) if isinstance(self.path_manager.selected_path, str) else self.path_manager.selected_path

        if not self.app_perms.check_perms(select_path):
            return

        self.open_file(select_path)

    def open_file(self, select_path):
        """
        Opens selected file (stub method).

        Args:
            path: Path to file to open.
        """
        if not self.file_redactor:
            self.close_window()
            return

        if not hasattr(self, 'file_redactor'):
            return

        self.file_redactor.settings_window = self.settings.settings_window
        self.file_redactor.create_window(
            self.settings.settings_window
        )

        if select_path is None:
            return

        self.file_redactor.file_path = select_path
        self.file_redactor.set_icon_image()

    def close_window(self) -> None:
        """Closes application and all additional windows."""
        self._settings_counts = self.settings_counts
        self._states = self.states
        try:
            if self.check_resource_exists(self.settings_configure):
                self.create_settings_configure(self.settings_configure)
        except Exception:
            pass

        self.settings.close_window()

        if self.root and self.root.winfo_exists():
            self.root.destroy()


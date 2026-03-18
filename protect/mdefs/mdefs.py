import json

import tkinter as tk

from pathlib import Path
from typing import List, Dict, Any
from functools import lru_cache
    
class MDEFSManager:
    """YPACMv1 security management framework.
    
    Args:
        root (tk.Tk): The root window of the application.
        app_gui (Any): Creates an interface for the main window.
        app_state (Any): Stores states flags (boolean).
        app_perms (Any): Analyzes the access rights of the current file.
        commands (Tuple): A tuple for storing service commands.
        perms_state (Any): Stores status flags (for permissions).
        path_manager (Any): Stores paths and lists of paths.
        search (Any): Generates lists of paths.
        system (Any): Provides paths to hide.
        select_state (Any): Stores the indexes of selected items of the list.
        select_position (Any): Returns the absolute path of the selected file.
        app_render (Any): Updates the application interface after operations.
    """

    def __init__(self, globals, callstack) -> None:
            self.globals = globals
            self.callstack = callstack

            self.root = self.globals['root']
            self.app_gui = self.callstack.app_gui
            self.app_state = self.callstack.app_state
            self.app_perms = self.callstack.app_perms
            self.app_render = self.callstack.app_render
            self.COMMANDS = self.globals['commands']
            self.file_extensions = self.globals['extensions']
            self.perms_state = self.callstack.perms_state
            self.path_manager = self.callstack.path_manager
            self.search = self.callstack.search_manager
            self.system = self.globals['system']
            self.select_state = self.callstack.select_state
            self.select_position = self.callstack.select_position

            self.paths: List[Path] = []
            self.symlinks: List[Path] = []

            self.config: Dict[str, Any] = {}
            self.paths_dict: Dict[str, Any] = {'paths': self.paths, 'symlinks': self.symlinks}
        
            self._progress_window: tk.Tk = self.progress_window
            self._notification_window: tk.Tk = self.notification_window

            self.callbacks: Dict[str, Any] = {
                'settings': None,
                'window': self._progress_window.window,
                'description': self._progress_window.description,
                'extensions': self.file_extensions,
                'progress': self._progress_window.progress,
                'length': self._progress_window.length,
                'mode': self._progress_window.mode,
                'process': self._progress_window.process,
                'close': self._progress_window.close,
                'finish': None,
                'update': None
            }

            self._pointer = self.pointer
            self._bootstrapper = self.bootstrapper
            self._delete_file = self.delete_file
            self._path_iterator = self.path_iterator
            self._access_manager = self.access_manager
            self._path_detector = self.path_detector
            self._rename_file = self.rename_file
            self._file_sorter = self.file_sorter

            self.callbacks['finish'] = self._path_detector.iteration
            self.app_render.callback = self.file_sorter_callback

            self._notification_window.create_window()
            self.load_config()

    @property
    @lru_cache
    def notification_window(self):
        """Imports the daemon window module."""
        from components.window.mdefs.notification_window import NotificationWindow
        return NotificationWindow(root=self.root)

    @property
    @lru_cache(maxsize=None)
    def progress_window(self):
        """Imports the process window module."""
        from components.window.progress.progress_window import ProgressWindow
        return ProgressWindow(root=self.root, app_gui=self.app_gui, 
            app_state=self.app_state)

    @property
    @lru_cache(maxsize=None)
    def pointer(self):
        """Imports the path generator module."""
        from protect.pointer.pointer import Pointer
        return Pointer(path_manager=self.path_manager, 
            select_position=self.select_position)

    @property
    @lru_cache(maxsize=None)
    def access_manager(self):
        """Imports the access verification module."""
        from protect.access.cwd.access_manager import AccessManager
        return AccessManager(root=self.root, 
            progress_window=self._progress_window, app_state=self.app_state, 
            callbacks=self.callbacks, path_iterator=self._path_iterator)
        
    @property
    @lru_cache(maxsize=None)
    def bootstrapper(self):
        """Imports the file creation module."""
        from protect.utils.bootstrapper.bootstrapper import Bootstrapper  
        return Bootstrapper(root=self.root, 
            notification_window=self._notification_window, 
            pointer=self._pointer, path_manager=self.path_manager, 
            callbacks=self.callbacks, search=self.search, 
            select_state=self.select_state, app_render=self.app_render)

    @property
    @lru_cache(maxsize=None)
    def delete_file(self):
        """Imports the file deletion module."""
        from protect.utils.delete.delete_file import DeleteFile
        return DeleteFile(app_perms=self.app_perms, 
            app_render=self.app_render, daemon=self._notification_window, 
            pointer=self._pointer, path_manager=self.path_manager, 
            search=self.search, select_state=self.select_state, 
            select_position=self.select_position, callbacks=self.callbacks)

    @property
    @lru_cache(maxsize=None)
    def rename_file(self):
        """Imports the file renaming module."""
        from protect.utils.rename.rename_file import RenameFile
        return RenameFile(app_render=self.app_render, 
            daemon=self._notification_window, path_manager=self.path_manager, 
            search=self.search, select_state=self.select_state, 
            callbacks=self.callbacks)

    @property
    @lru_cache
    def path_iterator(self):
        """Imports the file iteration module."""
        from protect.iterator.path_iterator import PathIterator
        return PathIterator(root=self.root, 
            progress_window=self.progress_window, app_state=self.app_state, 
            callbacks=self.callbacks, paths_dict=self.paths_dict)

    @property
    @lru_cache
    def path_detector(self):
        """Imports the file detection module."""
        from protect.detector.path_detector import PathDetector
        return PathDetector(root=self.root, app_state=self.app_state, 
            access_manager=self._access_manager, paths_dict=self.paths_dict)

    @property
    @lru_cache(maxsize=None)
    def file_sorter(self):
        """Imports the list sorting module."""
        from protect.sorter.file_sorter import FileSorter
        return FileSorter(app_state=self.app_state, app_perms=self.app_perms, 
            callbacks=self.callbacks, commands=self.COMMANDS, 
            pointer=self.pointer, perms_state=self.perms_state, 
            path_manager=self.path_manager, system=self.system)

    def load_config(self) -> None:
        """Loads configuration files."""
        parent_path = Path(__file__).parents[1]
        parts_catalog = parent_path / 'parts'
        config_path = parts_catalog / 'system_parts.json'
        
        with open(config_path, 'r', encoding='utf-8') as config:
            self.config = json.loads(config.read())

    def mdefs_pointer(self, command: str):
        """Generates a path to the current directory."""
        if command == 'add':
            self._pointer.add_point()
        elif command == 'pop':
            self._pointer.pop_point()
        elif command == 'root':
            self._pointer.root_point()
        elif command == 'clear':
            self._pointer.clear_points()

    def access(self, check_path: Path = 'YellowPather'):
        """Checks the access rights for the current file."""
        self._access_manager.access(check_path)
                
    def bootstrap(self, input_path: str = 'New Folder', 
        create_type: str = 'Folder') -> None:
            """Creates a new file at the specified path."""
            parent_path = self._pointer.catalog_path
            if parent_path is None:
                return

            absolute_path = parent_path / input_path
            create_path = (Path(absolute_path) 
                if isinstance(absolute_path, str) else absolute_path)
            self._bootstrapper.bootstrapper(input_path, create_path, create_type)

    def delete_file_callback(self, delete_path: Path) -> None:
        """Deletes a file at the specified path."""
        self._delete_file.delete_file(delete_path)

    def rename_file_callback(self, current_path: Path, rename_path: Path) -> None:
        """Renames a file at the specified path."""
        self._rename_file.rename_file(current_path, rename_path)

    def file_sorter_callback(self, paths: List[Path], root: Path, 
        path: Path = None, reverse: bool = True, sorting: str = 'disabled') -> None:
            """Sorts the list of items."""
            self._file_sorter.file_sorter(paths, root, path, reverse, sorting)

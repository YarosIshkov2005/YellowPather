import os
import textwrap

from pathlib import Path
from typing import List

class FileSorter:
    def __init__(self, app_state, app_perms, callbacks, commands, pointer, perms_state, path_manager, system) -> None:
        self.app_state = app_state
        self.app_perms = app_perms
        self.callbacks = callbacks
        self.COMMANDS = commands if commands is not None else ()
        self.pointer = pointer
        self.perms_state = perms_state
        self.path_manager = path_manager
        self.system = system

    def file_sorter(self, paths: List[Path], root: Path, 
        path: Path, reverse: bool, sorting: str):
        if sorting == 'Standart':
            hidden = self.system.catalogs
            self.add_paths(root, path, hidden)
            return

        if len(self.path_manager.abs_paths) <= 1:
            return

        sorting_type = {
            'By name': self.sorting_by_name,
            'By date': self.sorting_by_date,
            'By size': self.sorting_by_size
        }

        if not self.perms_state.hide_access_error:
            self.perms_state.hide_access_error = True

        if sorting != 'By name':
            checked = self.check_permssions(paths)
            items = sorting_type[sorting](checked, reverse)
            self.path_manager.abs_paths = items
            self.path_manager.rel_paths = self.rel_paths(items, root)
            self.path_manager.short_names = self.short_names(items)
        else:
            checked = self.check_permssions(paths)
            items = sorting_type[sorting](checked)
            self.path_manager.abs_paths = items
            self.path_manager.rel_paths = self.rel_paths(items, root)
            self.path_manager.short_names = self.short_names(items)

        if self.perms_state.hide_access_error:
            self.perms_state.hide_access_error = False

    def sorting_by_name(self, paths: List[Path]):
        return sorted(paths, key=lambda path: path.name.lower())

    def sorting_by_date(self, paths: List[Path], reverse: bool):
        return sorted(paths, key=lambda path: path.stat().st_mtime, reverse=reverse)

    def sorting_by_size(self, paths: List[Path], reverse: bool):
        return sorted(paths, key=lambda path: path.stat().st_size, reverse=reverse)

    def check_permssions(self, paths: List[Path]):
        items = []
        for entry in paths:
            if not self.app_perms.check_perms(entry):
                continue
            items.append(entry)

        return items

    def add_paths(self, root: Path, path: Path, hidden: Path) -> None:
        """Populates path lists for display."""
        self.path_manager.abs_paths.clear()
        self.path_manager.rel_paths.clear()
        self.path_manager.short_names.clear()

        self.path_manager.abs_paths = self.abs_paths(path, hidden)
        self.path_manager.rel_paths = self.rel_paths(
            self.path_manager.abs_paths, root)
        self.path_manager.short_names = self.short_names(self.path_manager.abs_paths)

    def abs_paths(self, path: Path, protect_catalogs: Path) -> list:
        """
        Gets list of absolute paths in specified directory.

        Args:
            path: Directory to iterate.
            protect_catalogs: List of directories to exclude.

        Returns:
            List of absolute paths in directory.
        """
        items = []
        path = Path(path) if isinstance(path, str) else path

        total_protects = len(protect_catalogs) - 1
        count = -1
            
        for entry in path.iterdir():
            if count < total_protects:
                count += 1

            if entry.name in self.COMMANDS:
                continue
                
            if entry.name in self.system.home:
                continue

            if entry.name in self.system.catalogs:
                continue

            path_str = str(entry)
            if len(protect_catalogs) > 0:
                protect_catalog = str(protect_catalogs[count])

                if path_str == protect_catalog:
                    continue
            items.append(entry)
        
        return items

    def rel_paths(self, paths: List[Path], root: Path) -> list:
        """
        Gets list of relative paths from base path.

        Args:
            root_path (Path): Base path for relative calculations.

        Returns:
            List of relative paths.
        """
        items = []
        for entry in paths:
            items.append(entry.relative_to(root))

        return items

    def short_names(self, paths: List[Path]) -> list:
        """
        Generates shortened names for display.

        Returns:
            List of shortened names with ellipsis if needed.
        """
        items = []
        for entry in paths:
            if entry.is_symlink():
                short_name = textwrap.shorten(
                    str(entry.name) + f'->{os.sep}', width=35, placeholder='...'
                )
            elif entry.is_dir():
                short_name = textwrap.shorten(
                    str(entry.name) + os.sep, width=35, placeholder='...'
                )
            elif entry.is_file():
                short_name = textwrap.shorten(
                    str(entry.name), width=35, placeholder='...'
                )
            items.append(short_name)

        return items

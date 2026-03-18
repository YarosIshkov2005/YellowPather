import os
import textwrap

from pathlib import Path

class SearchManager:
    """
    Search and file/directory processing class.

    Provides methods for file searching, directory iteration, and
    name processing for display.
    """

    def __init__(self, globals, callstack) -> None:
        """Initializes FileManagerSearch with empty lists."""
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.COMMANDS = self.globals['commands']
        self.path_manager = self.callstack.path_manager
        self.system = self.globals['system']
        
        self.total: int = 0

    def iteration_dir(self, path: Path, protect_catalogs: Path) -> list:
        """
        Gets list of absolute paths in specified directory.

        Args:
            path: Directory to iterate.
            protect_catalogs: List of directories to exclude.

        Returns:
            List of absolute paths in directory.
        """
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

            self.path_manager.abs_paths.append(entry)

        self.total = len(self.path_manager.abs_paths)
        
        return self.path_manager.abs_paths

    def iteration_name(self, root_path: Path) -> list:
        """
        Gets list of relative paths from base path.

        Args:
            root_path (Path): Base path for relative calculations.

        Returns:
            List of relative paths.
        """
        if root_path is None:
            return

        for entry in self.path_manager.abs_paths:
            self.path_manager.rel_paths.append(entry.relative_to(root_path))

        return self.path_manager.rel_paths

    def iteration_short_name(self) -> list:
        """
        Generates shortened names for display.

        Returns:
            List of shortened names with ellipsis if needed.
        """
        for entry in self.path_manager.abs_paths:
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
            self.path_manager.short_names.append(short_name)

        return self.path_manager.short_names

    def glob_search(self, path: Path, extension: str) -> list:
        """
        Non-recursive file search by extension.

        Args:
            path: Directory to search in.
            extension: File extension to search for.

        Returns:
            List of found file names.
        """
        self.path_manager.abs_paths.clear()
        self.path_manager.rel_paths.clear()
        self.path_manager.short_names.clear()

        for entry in path.glob(f"*{extension}"):
            self.path_manager.abs_paths.append(entry)

            short_name = textwrap.shorten(
                entry.name, width=35, placeholder='...'
            )
            self.path_manager.short_names.append(short_name)

        self.total = len(self.path_manager.short_names)
        
        return self.path_manager.short_names

    def rglob_search(self, path: Path, extension: str) -> list:
        """
        Recursive file search by extension.

        Args:
            path: Directory to search in.
            extension: File extension to search for.

        Returns:
            List of found file names.
        """
        self.path_manager.abs_paths.clear()
        self.path_manager.rel_paths.clear()
        self.path_manager.short_names.clear()

        for entry in path.rglob(f'*{extension}'):
            #if entry in protect_files:
                #continue

            root_path = str(self.path_manager.root_path)
            absolute_path = str(entry)
            resource = os.path.relpath(absolute_path, root_path)

            if 'YellowPather' in entry.parts:
                continue
            
            if resource in self.system.mdefs:
                continue
                
            if resource in self.system.home:
                continue
                
            if resource in self.system.catalogs:
                continue

            if resource in self.system.icons:
                continue
                
            if resource in self.system.files:
                continue
            
            self.path_manager.abs_paths.append(entry)

            short_name = textwrap.shorten(
                str(entry.name), width=35, placeholder='...'
            )
            self.path_manager.short_names.append(short_name)

        self.total = len(self.path_manager.short_names)
        
        return self.path_manager.short_names

    def add_paths(self) -> None:
        """Populates path lists for display."""
        self.path_manager.abs_paths.clear()
        self.path_manager.rel_paths.clear()
        self.path_manager.short_names.clear()

        self.path_manager.abs_paths = self.iteration_dir(self.path_manager.absolute_path, self.system.catalogs)
        self.path_manager.rel_paths = self.iteration_name(self.path_manager.root_path)
        self.path_manager.short_names = self.iteration_short_name()

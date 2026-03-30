# Standard libraries
import os
import shutil

# Third-party libraries
from tkinter.messagebox import showinfo, showerror

# Local modules
from typing import Optional, List, Dict, Any


class CommandExecuterCore:
    """Class of command executer."""

    def __init__(self, globals) -> None:
        self.globals = globals
        
        self.root = self.globals['root']

    def command_executer(
        self,
        parameters: Optional[Dict[str, Any]]
    ) -> Optional[bool]:
        """
        Manage commands.

        Args:
            parameters (Dict[str, Any]): user command, sources,
                                         destination, root, paths

        Returns:
            bool: True if the operation is successful,
                  False/None - on errors
        """
        try:
            if parameters is None:
                return None

            command = parameters['command']
            sources = parameters['sources']
            destination = parameters['destination']
            root = parameters['root']
            paths = parameters['paths']

            if command == 'copy':
                return self.copy_operation(sources, destination, root, paths)
            elif command == 'move':
                return self.move_operation(sources, destination, root, paths)
            elif command == 'rename':
                return self.rename_operation(sources, destination, root, paths)
            else:
                showerror(
                    title='Yellow Pather Error 014:',
                    message=f"Unknown command '{command}'",
                    parent=self.root
                )
                return None
        except Exception as e:
            showerror(
                title='Yellow Pather Error 014:',
                message=f'{e}',
                parent=self.root
            )
            return None

    def copy_operation(
        self,
        sources: List[str],
        destination: str,
        root: str,
        paths: List[str]
    ) -> bool:
        """
        Perform copying.

        Args:
            sources (List[str]): Paths of copied objects
            destination (str): Endpoint path
            root (str): Root path
            paths (List[str]): Real paths

        Returns:
            bool: True if the operation is successful,
                  False on errors
        """
        try:
            count = 0
            source_path = ''
            destination_path = os.path.join(root, destination)
            is_destination_catalog = os.path.isdir(destination_path)

            if not os.path.exists(destination_path):
                os.makedirs(destination_path, exist_ok=True)

            for source in sources:
                source_path = os.path.join(root, source)
                target_path = os.path.join(root, destination, source)

                if not os.path.exists(source_path):
                    error_msg = (
                        f"'{os.path.basename(source_path)}' "
                        "does not exist"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                elif not os.path.exists(destination_path):
                    error_msg = (
                        f"'{os.path.basename(destination_path)}' "
                        "does not exist"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                if source_path not in paths:
                    error_msg = (
                        f"'{os.path.basename(source_path)}' "
                        "not found"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                if source_path == destination_path:
                    error_msg = (
                        f"copy from '{os.path.basename(source_path)}' "
                        f"to '{os.path.basename(destination_path)}' "
                        "is not possible"
                    )
                    showerror(
                        title='Yellow Pather Error 014:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                try:
                    is_source_catalog = os.path.isdir(source_path)
                    is_source_file = os.path.isfile(source_path)

                    if is_source_catalog and is_destination_catalog:
                        shutil.copytree(source_path, target_path)
                    elif is_source_file and is_destination_catalog:
                        shutil.copy2(source_path, target_path)
                    else:
                        showerror(
                            title='Yellow Pather Error 020:',
                            message=f"Cannot copy to '{destination}'",
                            parent=self.root
                        )
                        continue

                    count += 1
                except FileExistsError:
                    error_msg = (
                        f"'{os.path.basename(destination_path)}' "
                        "already exists"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                except Exception as e:
                    showerror(
                        title='Yellow Pather Error 020:',
                        message=f'{e}',
                        parent=self.root
                    )

            if count > 0:
                info_msg = (
                    f"Copied '{count}' item(s) to "
                    f"'{os.path.basename(destination)}'"
                )
                showinfo(
                    title='Copied:',
                    message=info_msg,
                    parent=self.root
                )
                return True
            return False
        except Exception as e:
            showerror(
                title='Yellow Pather Error 020:',
                message=f'{e}',
                parent=self.root
            )
            return False

    def move_operation(
        self,
        sources: List[str],
        destination: str,
        root: str,
        paths: List[str]
    ) -> bool:
        """
        Perform moving.

        Args:
            sources (List[str]): Paths of moved objects
            destination (str): Endpoint path
            root (str): Root path
            paths (List[str]): Real paths

        Returns:
            bool: True if the operation is successful,
                  False on error
        """
        try:
            count = 0
            source_path = ''
            destination_path = os.path.join(root, destination)
            is_destination_catalog = os.path.isdir(destination_path)

            if not os.path.exists(destination_path):
                os.makedirs(destination_path, exist_ok=True)

            for source in sources:
                source_path = os.path.join(root, source)
                target_path = os.path.join(root, destination, source)

                if not os.path.exists(source_path):
                    error_msg = (
                        f"'{os.path.basename(source_path)}' "
                        "does not exist"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                elif not os.path.exists(destination_path):
                    error_msg = (
                        f"'{os.path.basename(destination_path)}' "
                        "does not exist"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                if source_path not in paths:
                    error_msg = (
                        f"'{os.path.basename(source_path)}' "
                        "not found"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                if source_path == destination_path:
                    error_msg = (
                        f"copy from '{os.path.basename(source_path)}' "
                        f"to '{os.path.basename(destination_path)}' "
                        "is not possible"
                    )
                    showerror(
                        title='Yellow Pather Error 020:',
                        message=error_msg,
                        parent=self.root
                    )
                    continue

                try:
                    is_source_catalog = os.path.isdir(source_path)
                    is_source_file = os.path.isfile(source_path)

                    if is_source_catalog and is_destination_catalog:
                        shutil.move(source_path, target_path)
                    elif is_source_file and is_destination_catalog:
                        shutil.move(source_path, target_path)
                    else:
                        showerror(
                            title='Yellow Pather Error 020:',
                            message=f"Cannot move to '{destination}'",
                            parent=self.root
                        )
                        continue

                    count += 1
                except FileExistsError:
                    error_msg = (
                        f"'{os.path.basename(destination_path)}' "
                        "already exists"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                except Exception as e:
                    showerror(
                        title='Yellow Pather Error 020:',
                        message=f'{e}',
                        parent=self.root
                    )

            if count > 0:
                info_msg = (
                    f"Moved '{count}' item(s) to "
                    f"'{os.path.basename(destination)}'"
                )
                showinfo(
                    title='Moved:',
                    message=info_msg,
                    parent=self.root
                )
                return True
            return False
        except Exception as e:
            showerror(
                title='Yellow Pather Error 020:',
                message=f'{e}',
                parent=self.root
            )
            return False

    def rename_operation(
        self,
        sources: List[str],
        destination: str,
        root: str,
        paths: List[str]
    ) -> bool:
        """
        Perform renaming.

        Args:
            sources (List[str]): Paths of renamed objects
            destination (str): Endpoint path
            root (str): Root path
            paths (List[str]): Real paths

        Returns:
            bool: True if the operation is successful,
                  False on error
        """
        try:
            for source in sources:
                source_path = os.path.join(root, source)
                target_path = os.path.join(root, destination)

                if source_path not in paths:
                    error_msg = (
                        f"'{os.path.basename(source_path)}' "
                        "not found"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    return False

                if source_path == target_path:
                    error_msg = (
                        f"Cannot rename from '{os.path.basename(source_path)}' "
                        f"to same name '{os.path.basename(target_path)}'"
                    )
                    showerror(
                        title='Yellow Pather Error 020:',
                        message=error_msg,
                        parent=self.root
                    )
                    return False

                try:
                    os.rename(source_path, target_path)
                    info_msg = (
                        f"Renamed '{os.path.basename(source_path)}' "
                        f"to '{os.path.basename(target_path)}'"
                    )
                    showinfo(
                        title='Renamed',
                        message=info_msg,
                        parent=self.root
                    )
                    return True
                except FileExistsError:
                    error_msg = (
                        f"'{os.path.basename(target_path)}' "
                        "already exists"
                    )
                    showerror(
                        title='Yellow Pather Error 009:',
                        message=error_msg,
                        parent=self.root
                    )
                    return False
                except Exception as e:
                    showerror(
                        title='Yellow Pather Error 020:',
                        message=f'{e}',
                        parent=self.root
                    )
                    return False
        except Exception as e:
            showerror(
                title='Yellow Pather Error 020:',
                message=f'{e}',
                parent=self.root
            )
            return False

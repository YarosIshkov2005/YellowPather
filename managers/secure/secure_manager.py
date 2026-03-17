import os

import tkinter as tk
from tkinter.messagebox import showinfo, showerror

from pathlib import Path
from typing import Optional
from enum import Enum, auto

class IsAnAttempt(Enum):
    IS_NOT_AN_ATTEMPT = auto()
    IS_AN_ATTEMPT = auto()

class SecureManager:
    """It prevents users from opening system directories without administrator priveleges."""
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.button_state = self.callstack.button_state
        self.counters = self.globals['counters']
        self.os_system = self.callstack.os_system
        self.system = self.globals['system']
        self.secure_state = self.callstack.secure_state

        self.PARENT_CATALOG: Optional[Path] = Path(__file__).parents[1]
        self.ROOT_CATALOG: Optional[Path] = Path(__file__).parents[2]
        self.WINDOWS_STORAGE: Optional[Path] = Path('c:\\')
        self.UNIX_STORAGE: Optional[Path] = Path('/')

        self.PATH_NAME = {
            'current': ['.\\', './'],
            'parent': ['..\\', '../']
        }

        # For manual input mode
        self.attempt_for_a_program_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT
        self.attempt_for_a_parent_program_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT

        self.attempt_for_a_windows_storage = IsAnAttempt.IS_NOT_AN_ATTEMPT
        self.attempt_for_a_unix_storage = IsAnAttempt.IS_NOT_AN_ATTEMPT

        # For main mode
        self.attempt_for_a_current_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT
        self.attempt_for_a_parent_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT

    def check_input_path(self, input_path: str, root_path: Path, check_path: Path) -> bool:
        """
        Checks whether the user-entered path points to the program's working or Windows root directory, and if so, prevents the user from accessing the current working directory.
        
        Args:
            input_path (str): The path entered by the user.
            root_path (Path): The path to the root directory.
            check_path (Path): The path entered by the user (corrected).
            
        Returns:
            True if the path does not point to the program's working directory, False otherwise.
        """
        try:
            if not self.check_access_attempt(input_path, root_path, check_path):
                return True

            self.button_state.update_search_state()
            return False
        except Exception as e:
            showerror(title='Yellow Pather Error 004:', message=f'{e}', parent=self.root)
            return False

    def reset_attempt_state(self):
        """Resets the detection status before use."""
        self.attempt_for_a_program_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT
        self.attempt_for_a_parent_program_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT

        self.attempt_for_a_windows_storage = IsAnAttempt.IS_NOT_AN_ATTEMPT
        self.attempt_for_a_unix_storage = IsAnAttempt.IS_NOT_AN_ATTEMPT

        self.attempt_for_a_current_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT
        self.attempt_for_a_parent_catalog = IsAnAttempt.IS_NOT_AN_ATTEMPT

    def protect_system_storage(self, check_path: Path) -> None:
        """Checks whether the path to the Windows or UNIX storage.
        
        Args:
            check_path (Path): The absolute path to the current object.
        """
        system_tuple = self.os_system.get_system()
        system = system_tuple[0]

        if system == 'Windows':
            if self.protect_windows_storage(check_path):
                self.attempt_for_a_windows_storage = IsAnAttempt.IS_AN_ATTEMPT

        elif system in ['Darwin', 'Linux']:
            if self.protect_unix_storage(check_path):
                self.attempt_for_a_unix_storage = IsAnAttempt.IS_AN_ATTEMPT

    def check_access_attempt(self, input_path: str, root_path: Path, check_path: Path) -> bool:
        """Calls the validation methods for the received path and records the attempt status.
        
        Args:
            input_path (str): The string entered by the user.
            root_path (Path): The path to the root directory of the device or program.
            check_path (Path): The absolute path to the current object.
            
        Returns:
            True if at least one of the attempst was detected, False otherwise.
        """
        self.reset_attempt_state()

        self.protect_system_storage(check_path)

        if self.protect_program_catalog(check_path):
            self.attempt_for_a_program_catalog = IsAnAttempt.IS_AN_ATTEMPT

        if self.protect_parent_program_catalog(check_path):
            self.attempt_for_a_parent_program_catalog = IsAnAttempt.IS_AN_ATTEMPT

        if self.protect_current_catalog(input_path, root_path, check_path):
            self.attempt_for_a_current_catalog = IsAnAttempt.IS_AN_ATTEMPT

        if self.protect_parent_catalog(input_path, root_path, check_path):
            self.attempt_for_a_parent_catalog = IsAnAttempt.IS_AN_ATTEMPT

        if (self.attempt_for_a_program_catalog == IsAnAttempt.IS_AN_ATTEMPT 
            or self.attempt_for_a_parent_program_catalog == IsAnAttempt.IS_AN_ATTEMPT 
            or self.attempt_for_a_windows_storage == IsAnAttempt.IS_AN_ATTEMPT 
            or self.attempt_for_a_unix_storage == IsAnAttempt.IS_AN_ATTEMPT 
            or self.attempt_for_a_current_catalog == IsAnAttempt.IS_AN_ATTEMPT 
            or self.attempt_for_a_parent_catalog == IsAnAttempt.IS_AN_ATTEMPT):
            return True
        return False

    def protect_program_catalog(self, check_path: Path) -> bool:
        """Check whether the entered path points to the current directory (manual mode).
        
        Args:
            check_path (Path): The absolute path to the current object.
            
        Returns:
            True if the path points to the current directory, False otherwise.
        """
        user_input_path = Path(check_path) if isinstance(check_path, str) else check_path
        is_program_path = False

        try:
            is_program_path = user_input_path.samefile(self.PARENT_CATALOG)
        except (FileNotFoundError, OSError):
            is_program_path = (user_input_path.resolve().as_posix().lower() ==
                            self.PARENT_CATALOG.resolve().as_posix().lower())

        if not is_program_path:
            return False

        if self.secure_state.hide_storage_error:
            return True

        showerror(
            title='Yellow Pather Error 011:',
            message=f"Permission Error: an attempt to enter the program directory '{str(self.PARENT_CATALOG) + os.sep}'",
            parent=self.root
        )
        self.app_gui.path_entry.focus()
        return True

    def protect_parent_program_catalog(self, check_path: Path) -> bool:
        """Checks whether the path points to the parent directory (manual mode).
        
        Args:
            check_path (Path): The absolute path to the current object.
            
        Returns:
            True if the path points to the parent directory, False otherwise.
        """
        user_input_path = Path(check_path) if isinstance(check_path, str) else check_path
        is_parent_program_path = False

        if not user_input_path.exists():
            showerror(
                title='Yellow Pather Error 009:',
                message=f"Path Error: '{user_input_path}' does not exist",
                parent=self.root
            )
            return

        try:
            is_parent_program_path = user_input_path.samefile(self.ROOT_CATALOG)
        except (FileNotFoundError, OSError):
            is_parent_program_path = (user_input_path.resolve().as_posix().lower() ==
                            self.ROOT_CATALOG.resolve().as_posix().lower())

        if not is_parent_program_path:
            return False

        if self.secure_state.hide_storage_error:
            return True

        showerror(
            title='Yellow Pather Error 011:',
            message=f"Permission Error: an attempt to enter the parent program directory '{str(self.ROOT_CATALOG) + os.sep}'",
            parent=self.root
        )
        self.app_gui.path_entry.focus()
        return True

    def protect_windows_storage(self, check_path: Path) -> bool:
        """Checks whether the path to the Windows drive is specified.
        
        Args:
            check_path (Path): The absolute path to the current object.
            
        Returns:
            True if the path points to the Windows drive, False otherwise.
        """
        user_input_path = Path(check_path) if isinstance(check_path, str) else check_path
        is_windows_storage_path = False

        try:
            is_windows_storage_path = user_input_path.samefile(self.WINDOWS_STORAGE)
        except (FileNotFoundError, OSError):
            is_windows_storage_path = (user_input_path.resolve().as_posix().lower() ==
                            self.WINDOWS_STORAGE.resolve().as_posix().lower())

        if not is_windows_storage_path:
            return False

        if self.secure_state.hide_storage_error:
            return True

        showerror(
            title='Yellow Pather Error 011:',
            message=f"Permission Error: an attempt to enter the root Windows directory '{str(self.WINDOWS_STORAGE)}'",
            parent=self.root
        )
        self.app_gui.path_entry.focus()
        return True

    def protect_unix_storage(self, check_path: Path) -> bool:
        """Checks whether the path to the UNIX storage directory.
        
        Args:
            check_path (Path): The absolute path to the current object.
            
        Returns:
            True if the path points to the UNIX storage directory, False otherwise.
        """
        user_input_path = Path(check_path) if isinstance(check_path, str) else check_path
        is_unix_storage_path = False

        try:
            is_unix_storage_path = user_input_path.samefile(self.UNIX_STORAGE)
        except (FileNotFoundError, OSError):
            is_unix_storage_path = (user_input_path.resolve().as_posix().lower() ==
                            self.UNIX_STORAGE.resolve().as_posix().lower())

        if not is_unix_storage_path:
            return False

        if self.secure_state.hide_storage_error:
            return True

        showerror(
            title='Yellow Pather Error 011:',
            message=f"Permission Error: an attempt to enter the root UNIX directory '{str(self.UNIX_STORAGE)}'",
            parent=self.root
        )
        self.app_gui.path_entry.focus()
        return True

    def protect_current_catalog(self, input_path: str, root_path: Path, check_path: Path) -> bool:
        """Checks whether the path to the current directory (main mode).
        
        Args:
            input_path (str): The string entered by the user.
            root_path (Path): The path to the devices current directory or program.
            check_path (Path): The absolute path to the current object.
            
        Returns:
            True if the path points to the current directory, False otherwise.
        """
        user_input_path = Path(check_path) if isinstance(check_path, str) else check_path
        is_current_catalog_path = False

        input_path_parts = [part for part in input_path.split(os.sep) if part]

        if len(input_path_parts) == 0:
            return False

        input_path_name = input_path_parts[-1]

        if not input_path_name.endswith(os.sep):
            input_path_name = input_path_name + os.sep

        path_name = self.PATH_NAME['current']

        if input_path_name not in path_name:
            return False

        try:
            is_current_catalog_path = user_input_path.samefile(root_path)
        except (FileNotFoundError, OSError):
            is_current_catalog_path = (user_input_path.resolve().as_posix().lower() ==
                            root_path.resolve().as_posix().lower())

        if not is_current_catalog_path:
            return False

        if self.secure_state.hide_storage_error:
            return True

        showinfo(
            title='Message:',
            message='You are already in the root directory!',
            parent=self.root
        )
        self.app_gui.path_entry.focus()
        return True

    def protect_parent_catalog(self, input_path: str, root_path: Path, check_path: Path) -> bool:
        """Checks whether the path to the parent directory (main mode).
        
        Args:
            input_path (str): The string entered by the user.
            root_path (Path): The path to the devices parent directory or program.
            check_path (Path): The absolute path to the current object.
            
        Returns:
            True if the path points to the parrent directory, False otherwise.
        """
        root_path = root_path.parent
        user_input_path = Path(check_path) if isinstance(check_path, str) else check_path
        is_parent_catalog_path = False

        input_path_parts = [part for part in input_path.split(os.sep) if part]

        if len(input_path_parts) == 0:
            return False

        input_path_name = input_path_parts[-1]

        if not input_path_name.endswith(os.sep):
            input_path_name = input_path_name + os.sep

        path_name = self.PATH_NAME['parent']

        if input_path_name not in path_name:
            return False

        try:
            is_parent_catalog_path = user_input_path.samefile(root_path)
        except (FileNotFoundError, OSError):
            is_parent_catalog_path = (user_input_path.resolve().as_posix().lower() ==
                            root_path.resolve().as_posix().lower())

        if not is_parent_catalog_path:
            return False

        if self.secure_state.hide_storage_error:
            return True

        showerror(
            title='Yellow Pather Error 011:',
            message=f"Permission Error: an attempt to enter the parent directory '{str(root_path) + os.sep}'",
            parent=self.root
        )
        self.app_gui.path_entry.focus()
        return True

    def protect_catalog_detector(self, check_path: Path) -> bool:
        """
        Checks if path is in protected directory list (for search).
        
        Args:
            check_path (Path): Path to check.
            
        Returns:
            True if path is protected, False otherwise.
        """
        if self.app_state.resolve_work_main:
            return False
            
        check_parts = check_path.parts
        path_parts = [part for part in check_parts if part]

        hidden_paths = self.system.catalogs
        hide_parts = [Path(path).name for path in hidden_paths if path]

        for part in path_parts:
            if part in hide_parts:
                showerror(
                    title='Yellow Pather Error 011:',
                    message=f"Permission denied: '{part}'",
                    parent=self.root
                )

                self.button_state.update_search_state()

                if self.app_state.manual_input_mode:
                    if not self.app_state.root_path_correct:
                        self.app_gui.path_entry.delete(0, tk.END)
                        self.app_gui.path_entry.focus()

                        self.counters['root_position'] = self.app_gui.path_entry.index(tk.INSERT)
                        self.counters['start_position'] = self.app_gui.path_entry.index(tk.INSERT)
                    else:
                        self.app_gui.path_entry.delete(self.counters['start_position'], tk.END)
                        self.app_gui.path_entry.focus()
                    return True
        return False

    def home_catalog_detector(self, check_path: Path) -> bool:
        """
        Checks if path is in protected directory list (for home).

        Args:
            check_path: Path to check.

        Returns:
            True if path is protected, False otherwise.
        """
        if self.app_state.resolve_work_main:
            return False
            
        check_parts = check_path.parts
        path_parts = [part for part in check_parts if part]

        hidden_paths = self.system.home
        hide_parts = [Path(path).name for path in hidden_paths if path]

        for part in path_parts:
            if part in hide_parts:
                showerror(
                    title='Yellow Pather Error 011:',
                    message=f"Permission denied: '{part}'",
                    parent=self.root
                )

                self.button_state.update_search_state()

                self.app_gui.path_entry.delete(self.counters['start_position'], tk.END)
                self.app_gui.path_entry.focus()
                return True
        return False

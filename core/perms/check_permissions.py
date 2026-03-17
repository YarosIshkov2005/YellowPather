import os
import stat

from tkinter.messagebox import showerror

from pathlib import Path

class CheckPermissionsCore:
    def __init__(self, globals, callstack):
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.app_render = self.callstack.app_render
        self.button_state = self.callstack.button_state
        self.counters = self.globals['counters']
        self.COMMANDS = self.globals['commands']
        self.os_system = self.callstack.os_system
        self.perms_state = self.callstack.perms_state
        self.path_manager = self.callstack.path_manager
        self.select_state = self.callstack.select_state
        self.secure_manager = self.callstack.secure_manager
       
    def check_permission(self, check_path: Path) -> bool:
        """
        Checks access permissions for specified path.

        Args:
            check_path: Path to check permissions for.

        Returns:
            True if accessible, False otherwise.
        """
        try:
            check_path = Path(check_path) if isinstance(check_path, str) else check_path
            
            if self.path_not_exists(check_path):
                return False

            if self.path_is_file(check_path):
                return False

            if not self.check_perms(check_path):
                return False
            return True
        except Exception as e:
            perms = self.permission_detector(check_path)
            showerror(
                title='Yellow Pather Error 004:',
                message=f"Permission Error: '{e}' (current: {perms})",
                parent=self.root
            )
            return False

    def path_not_exists(self, check_path):
        try:
            if check_path.exists():
                return False

            path_name = check_path.name
            short_name = self.app_render.safe_popup_truncate(path_name)

            if self.app_state.is_string_active:
                return False

            if path_name in self.COMMANDS:
                return False
                    
            if check_path.is_dir() or check_path.is_file():
                return False

            if not self.perms_state.hide_file_error:
                showerror(
                    title='Yellow Pather Error 009:',
                    message=f"Exist Error: '{short_name}' not exist",
                    parent=self.root
                )
                
            self.app_gui.path_entry.focus()
            return True
        except Exception as e:
            perms = self.permission_detector(check_path)
            showerror(
                title='Yellow Pather Error 004:',
                message=f"Permission Error: '{e}' (current: {perms})",
                parent=self.root
            )
            return False

    def path_is_file(self, check_path):
        try:
            if not check_path.is_file():
                return False

            path_name = check_path.name
            short_name = self.app_render.safe_popup_truncate(path_name)

            if not self.perms_state.hide_file_error:
                showerror(
                    title='Yellow Pather Error 010:',
                    message=f"File Error: '{short_name}' is file!",
                    parent=self.root
                )

            self.button_state.update_search_state()

            self.app_gui.path_entry.focus()
            return True
        except Exception as e:
            perms = self.permission_detector(check_path)
            showerror(
                title='Yellow Pather Error 004:', 
                message=f"Permission Error: '{e}' (current: {perms})", 
                parent=self.root
            )
            return False

    def check_perms(self, check_path):
        try:
            system_tuple = self.os_system.get_system()
            system = system_tuple[0]

            if system == 'Windows':
                try:
                    if check_path.is_dir():
                        list(check_path.iterdir())
                        test_file = check_path / '_test_file.tmp'
                        test_file.touch(exist_ok=False)
                        test_file.unlink()
                        return True
                    elif check_path.is_file():
                        with open(check_path, 'rb') as file:
                            file.read(1)
                        return True
                except (PermissionError, OSError, WindowsError):
                    perms = self.permission_detector(check_path)
                    path_name = check_path.name
                    short_name = self.app_render.safe_popup_truncate(path_name)

                    if check_path.samefile(self.secure_manager.WINDOWS_STORAGE):
                        short_name = str(self.secure_manager.WINDOWS_STORAGE)

                    if not self.perms_state.hide_access_error:
                        showerror(
                            title='Yellow Pather Error 004:',
                            message=f"Permission Error: permission denied '{short_name}' (current: {perms})",
                            parent=self.root
                        )

                    self.app_gui.path_entry.focus()

                    if not self.app_state.manual_input_mode:
                        self.button_state.update_search_state()
                    return False
            elif system in ['Darwin', 'Linux']:
                try:
                    if not os.access(check_path, os.R_OK | os.W_OK):
                        raise PermissionError
                    return True
                except (PermissionError, OSError):
                    perms = self.permission_detector(check_path)
                    path_name = check_path.name
                    short_name = self.app_render.safe_popup_truncate(path_name)

                    if check_path.samefile(self.secure_manager.UNIX_STORAGE):
                        short_name = str(self.secure_manager.UNIX_STORAGE)

                    if not self.perms_state.hide_access_error:
                        showerror(
                            title='Yellow Pather Error 004:',
                            message=f"Permission Error: permission denied  '{short_name}' (current: {perms})",
                            parent=self.root
                        )

                    self.app_gui.path_entry.focus()

                    if not self.app_state.manual_input_mode:
                        self.button_state.update_search_state()
                    return False
        except Exception as e:
            perms = self.permission_detector(check_path)
            showerror(
                title='Yellow Pather Error 004:',
                message=f"Permission Error: '{e}' (current: {perms})",
                parent=self.root
            )
            return False

    def permission_detector(self, check_path: Path) -> str:
        try:
            """
            Returns permissions in UNIX-style (chmod) format.

            Args:
                check_path: Path to check permissions for.

            Returns:
                Permission string in octal format.
            """
            path_stat = os.stat(check_path)
            return oct(stat.S_IMODE(path_stat.st_mode))
        except Exception as e:
            showerror(title='Yellow Pather Error 004:', message=f'Permission Error: {e}', parent=self.root)

from tkinter.messagebox import showerror

from pathlib import Path

class InputManager:
    def __init__(self, root, app_gui, app_state, secure_state, secure_manager, app_perms, mdefs) -> None:
        self.root = root
        self.app_gui = app_gui
        self.app_state = app_state
        self.secure_state = secure_state
        self.secure_manager = secure_manager
        self.app_perms = app_perms
        self.mdefs = mdefs

        self.user_path: str = ''

    def input_user_path(self) -> bool:
        """
        Validates root path correctness.

        Returns:
            True if root path is valid, False otherwise.
        """
        if self.secure_state.hide_storage_error:
            self.secure_state.hide_storage_error = False

        if not self.app_state.path_not_correct:
            self.app_state.path_not_correct = True
            return {}
            
        self.user_path = self.app_gui.path_entry.get()
        if not self.check_length_string(self.user_path):
            return {}

        if self.user_path == 'Here is your root path':
            return {}

        if not self.app_perms.check_permission(self.user_path):
            return {}

        if not self.secure_manager.check_input_path(self.user_path, Path(self.user_path), Path(self.user_path)):
            return {}

        return {
            'root_path': self.user_path
        }

    def check_length_string(self, check_string: str) -> bool:
        """
        Checks whether anything has been entered in the input field.
        
        Args:
            check_string: The string by the user.
            
        Returns:
            True if at least one character is intered, False otherwise.
        """
        string_length = len(check_string)

        if string_length == 0:
            showerror(
                title='Yellow Pather Error 016:',
                message=f"Input Error: The string cannot be empty (current length: {string_length})",
                parent=self.root
            )
            return False
        return True
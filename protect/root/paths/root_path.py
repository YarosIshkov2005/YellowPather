from tkinter.messagebox import showerror

from pathlib import Path

class RootPath:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.input_manager = self.callstack.input_manager
        self.path_manager = self.callstack.path_manager
        self.system_manager = self.callstack.system_manager

    def return_root_path(self) -> bool:
        """
        Prepares and validates root path.

        Returns:
            Root path if root path exists, None otherwise.
        """
        root_config = self.system_manager.check_root_path()
        root_path = root_config.get('root_path', 'system')

        if root_path == 'system':
            user_path = self.input_manager.input_user_path()
            root_path = user_path.get('root_path', 'system')

        if root_path == 'system':
            showerror(
                title='Yellow Pather Error 012:',
                message='Root path was not found',
                parent=self.root
            )
            return None

        self.path_manager.root_path = Path(root_path)

        return root_path

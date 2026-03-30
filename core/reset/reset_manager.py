import os

from tkinter.messagebox import showerror

class ResetManager:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.button_state = self.callstack.button_state
        self.catalog_detector = self.callstack.catalog_detector
        self.insert_manager = self.callstack.insert_manager
        self.framework = self.callstack.framework
        self.path_manager = self.callstack.path_manager
        self.secure_manager = self.callstack.secure_manager

    def reset_path(self) -> None:
        """Resets current path to root path."""
        if (self.app_state.is_parser_active or 
            self.app_state.is_recursive_search):
            self.insert_manager.clear_path()
            
        if self.app_state.is_search_executed:
            self.app_state.is_search_executed = False

        if not self.app_state.reset_button_active:
            self.app_state.reset_button_active = True

        if self.app_state.manual_input_mode:
            user_input = self.app_gui.path_entry.get()

            if len(user_input) == 0:
                showerror(
                    title='Yellow Pather Error 016:',
                    message='It is impossible to clear an empty line!',
                    parent=self.root
                )
                self.app_gui.path_entry.focus()
                return

            if (str(self.path_manager.absolute_path) + os.sep 
                in self.secure_manager.PATH_NAME.get('current')):
                return

        if (not self.app_state.is_recursive_search and 
            not self.app_state.is_parser_active and 
            self.catalog_detector.root_directory_detector(
            self.path_manager.root_path, self.path_manager.absolute_path)):
            self.app_gui.path_entry.focus()
            self.button_state.update_search_state()
            return

        if not self.app_state.is_root_directory:
            self.app_state.is_root_directory = True

        if self.app_state.is_recursive_search:
            self.app_state.is_recursive_search = False

        self.framework._mdefs_framework.mdefs_pointer('clear')
        self.framework._mdefs_framework.mdefs_pointer('root')

        self.app_state.is_search_active = False

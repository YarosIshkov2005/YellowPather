import os

from pathlib import Path

class UpdatePaths:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.app_state = self.callstack.app_state
        self.history_manager = self.callstack.history_manager
        self.mdefs = self.callstack.framework
        self.path_manager = self.callstack.path_manager
        self.root_manager = self.callstack.root_manager

    def set_paths(self):
        root_path = self.root_manager.return_root_path()
        absolute_path = root_path
        selected_path = root_path

        self.path_manager.root_path = root_path
        self.path_manager.absolute_path = root_path
        self.path_manager.resource_path = root_path
        self.path_manager.input_path = str(absolute_path) + os.sep

        self.mdefs._mdefs_framework.mdefs_pointer('root')
        self.history_manager.push(0)

        return {
            'root': root_path,
            'absolute': absolute_path,
            'selected': selected_path
        }

    def update_paths(self):
        current = self.globals['positions']['index']
        absolute_path = None
        selected_path = None

        if self.path_manager.short_names:
            selected_path = self.path_manager.abs_paths[current]
            absolute_path = selected_path.parent
            catalog_path = absolute_path

            self.path_manager.create_path = catalog_path
            self.path_manager.delete_path = selected_path
            self.path_manager.rename_path = selected_path
        else:
            absolute_path = self.path_manager.absolute_path
            self.path_manager.create_path = absolute_path

        if self.app_state.reset_button_active:
            self.path_manager.resource_path = self.path_manager.abs_paths[0]
            self.app_state.reset_button_active = False

        return {
            'absolute': absolute_path,
            'selected': selected_path
        }

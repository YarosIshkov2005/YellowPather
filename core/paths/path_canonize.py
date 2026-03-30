from pathlib import Path
from typing import Optional

class PathCanonize:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_state = self.callstack.app_state
        self.app_perms = self.callstack.app_perms
        self.app_render = self.callstack.app_render
        self.breadcrumbs = self.callstack.breadcrumbs
        self.history_manager = self.callstack.history_manager
        self.insert_manager = self.callstack.insert_manager
        self.path_manager = self.callstack.path_manager
        self.search_manager = self.callstack.search_manager
        self.select_state = self.callstack.select_state
        self.transitions = self.callstack.transitions
        self.root_manager = self.callstack.root_manager
        self.update_paths = self.callstack.update_paths
        self.update_resources = self.callstack.update_resources
        self.update_positions = self.callstack.update_positions

        self.root_path: Optional[Path] = None
        self.absolute_path: Optional[Path] = None
        self.selected_path: Optional[Path] = None
        self.navigation_path: Optional[Path] = None

        self.globals['update'] = self

    def canonizer(self, command: str = 'current'):
        current = self.globals['positions']['index']

        self.history_manager.set(command, current)
        self.transitions.transition(self.root_path, self.selected_path, command)

        self.update_resources.update_resources(self.root_path, 
        self.absolute_path, command)
        self.update_paths_callback()
        self.canonize_path()

    def set_paths_callback(self, command: str = 'current'):
        paths = self.update_paths.set_paths()
        self.root_path = paths['root']
        self.absolute_path = paths['absolute']
        self.selected_path = paths['selected']

        self.insert_manager.insert_path(self.root_path, 0, True)
        self.insert_manager.set_positions()

        self.update_resources.update_resources(self.root_path, 
        self.absolute_path, command)
        self.update_paths_callback()
        self.canonize_path()

    def update_paths_callback(self):
        paths = self.update_paths.update_paths()
        self.absolute_path = paths['absolute']
        self.selected_path = paths['selected']

    def canonize_path(self):
        if (self.app_state.is_recursive_search 
            or self.app_state.is_parser_active):
            self.update_positions.update_position()
            return

        if not self.app_state.insert_resource_name:
            if self.globals['breadcrumbs']['points']:
                self.navigation_path = self.absolute_path.relative_to(self.root_path)
            else:
                self.navigation_path = Path('.')
        else:
            self.navigation_path = self.selected_path.relative_to(self.root_path)

        self.path_manager.input_path = str(self.absolute_path)
        self.path_manager.selected_path = None
        self.path_manager.current_path = None

        self.app_render.canonize_entered_path(self.navigation_path)
        self.update_positions.update_position()

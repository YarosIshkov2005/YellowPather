from pathlib import Path

class UpdateResources:
    def __init__(self, callstack) -> None:
        self.callstack = callstack

        self.app_state = self.callstack.app_state
        self.app_render = self.callstack.app_render
        self.path_manager = self.callstack.path_manager
        self.search_manager = self.callstack.search_manager

    def update_resources(self, root_path: Path, absolute_path: Path, 
        command: str = 'render'):
        if self.app_state.block_when_update:
            self.path_manager.resource_path = absolute_path
        elif self.app_state.is_recursive_search:
            self.path_manager.resource_path = self.path_manager.pattern_path

        if self.app_state.reset_button_active:
            self.path_manager.resource_path = root_path
        elif self.app_state.search_button_active:
            self.path_manager.resource_path = self.path_manager.absolute_path
        elif self.app_state.settings_button_active:
            self.path_manager.resource_path = absolute_path

        if command == 'render':
            if not self.app_state.is_recursive_search:
                self.search_manager.add_paths()
            self.app_render.update_select_window()
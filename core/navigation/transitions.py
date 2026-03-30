from pathlib import Path

class Transitions:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.app_state = self.callstack.app_state
        self.app_perms = self.callstack.app_perms
        self.breadcrumbs = self.callstack.breadcrumbs
        self.mdefs = self.callstack.framework
        self.path_manager = self.callstack.path_manager
        self.history_manager = self.callstack.history_manager

    def transition(self, root_path: Path, selected_path: Path, 
        command: str = 'current'):
        current = self.globals['positions']['index']
        if command == 'current':
            return

        if self.app_state.search_button_active:
            self.app_state.is_search_active = True
            self.mdefs._mdefs_framework.mdefs_pointer('add')
            self.breadcrumbs.generate_breadcrumbs(root_path, 
            self.path_manager.absolute_path)
            self.history_manager.reset()

        elif self.app_state.next_button_active:
            absolute_path = self.path_manager.abs_paths[current]
            if not self.app_perms.check_permission(absolute_path):
                return

            self.mdefs._mdefs_framework.mdefs_pointer('add')

            self.breadcrumbs.generate_breadcrumbs(root_path, 
            selected_path)
            self.history_manager.push(0)

        elif self.app_state.back_button_active:
            if self.app_state.is_search_active:
                if len(self.globals['select']['points']) == 1:
                    self.app_state.is_search_active = False
                    self.mdefs._mdefs_framework.mdefs_pointer('root')
                    self.breadcrumbs.clear_points()
                    self.history_manager.reset()
                    return

            self.mdefs._mdefs_framework.mdefs_pointer('pop')

            self.breadcrumbs.parent_point()
            self.history_manager.pop()

        elif self.app_state.reset_button_active:
            self.breadcrumbs.clear_points()
            self.history_manager.reset()

            self.mdefs._mdefs_framework.mdefs_pointer('root')

        elif self.app_state.block_when_update:
            self.history_manager.reset()
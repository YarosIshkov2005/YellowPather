from tkinter.messagebox import showerror

from pathlib import Path

class Breadcrumbs:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_state = self.callstack.app_state
        self.path_manager = self.callstack.path_manager

    def generate_breadcrumbs(self, root_path: Path, absolute_path: Path):
        self.path_manager.absolute_path = absolute_path
        self.path_manager.resource_path = absolute_path
        self.generate_points(root_path, absolute_path)

    def get_points(self):
        return self.globals['breadcrumbs']['points']

    def parent_point(self):
        if not self.globals['breadcrumbs']['points']:
            if not self.app_state.is_root_directory:
                self.app_state.is_root_directory = True
                self.path_manager.absolute_path = self.path_manager.root_path
            return

        if self.globals['breadcrumbs']['points']:
            self.globals['breadcrumbs']['points'].pop()

        parent_path = self.path_manager.root_path
        for point in self.globals['breadcrumbs']['points']:
            parent_path /= point

        self.path_manager.absolute_path = parent_path
        self.path_manager.resource_path = parent_path

    def clear_points(self):
        if self.globals['breadcrumbs']['points']:
            self.globals['breadcrumbs']['points'].clear()

        self.path_manager.absolute_path = self.path_manager.root_path
        self.path_manager.resource_path = self.path_manager.root_path

    def generate_points(self, root_path: Path, absolute_path: Path) -> None:
        """Generates breadcrumb navigation points."""
        try:
            relative_path = absolute_path.relative_to(root_path)
            self.globals['breadcrumbs']['points'] = [point for point in 
                relative_path.parts if point and point != '.']
        except Exception as e:
            showerror(title='Yellow Pather Error 005:', 
                message=f'{e}', parent=self.root)

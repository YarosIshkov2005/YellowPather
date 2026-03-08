import tkinter as tk

from tkinter.messagebox import showerror

from functools import lru_cache
from typing import Any, Optional

class SettingsManager:
<<<<<<< HEAD
    def __init__(self, settings, settings_gui, mdefs, search, app_render, select_position) -> None:
=======
    def __init__(self, counters, settings, settings_gui, mdefs, path_manager, states, search, app_state, app_render, select_position) -> None:
        self.counters = counters
>>>>>>> f38613a (Version 1.0.2)
        self.settings = settings
        self.settings_gui = settings_gui
        self.mdefs = mdefs
        self.path_manager = path_manager
        self.states = states
        self.search = search
        self.app_state = app_state
        self.app_render = app_render
        self.select_position = select_position

        self.settings_window: Optional[tk.Tk] = None
        self.create_type: Any = self.states['create']
        self.sort_type: Any = self.states['sorting']
        self.type_count: int = self.counters['create_position']
        self.sort_count: int = self.counters['sort_position']

        self._rename_window = self.rename_window
        self._rename_window.callbacks['create'] = self.create_new_resource
        self._rename_window.callbacks['rename'] = self.rename_file

    @property
    @lru_cache(maxsize=None)
    def rename_window(self):
        from components.window.rename.rename_window import RenameWindow
        return RenameWindow(root=self.settings_window)

    def back_type(self):
        self.type_count -= 1
        if self.type_count == -1:
            self.type_count = 1

        self.counters['create_position'] = self.type_count
        self.select_create_type()

    def select_create_type(self):
        if self.counters['create_position'] == 0:
            self.states['create'] = 'catalog'
        else:
            self.states['create'] = 'file'
        self.create_type = self.states['create']
        self.settings_gui.select_type.config(text=f'    {self.create_type}    ')

    def next_type(self):
        self.type_count += 1
        if self.type_count == 2:
            self.type_count = 0

        self.counters['create_position'] = self.type_count
        self.select_create_type()

    def create_rename_window(self, target: str):
        self._rename_window.target = target
        self._rename_window.create_window()

    def create_new_resource(self, new_path: str = ''):
        try:
            self.mdefs._mdefs_framework.bootstrap(new_path, self.create_type)
            self._rename_window.close_window()
        except Exception as e:
            showerror(title='Yellow Pather Error 009:', message=f'{e}', parent=self.settings_window)

    def delete_select_resource(self):
        try:
            catalog_path = self.mdefs._mdefs_framework._pointer.catalog_path
            relative_path = self.select_position.relative_path
            delete_path = catalog_path / relative_path

            self.mdefs._mdefs_framework.delete_file_callback(delete_path)
        except Exception as e:
            showerror(title='Yellow Pather Error 009:', message=f'{e}', parent=self.settings_window)

    def rename_file(self, user_input: str):
        try:
            catalog_path = self.mdefs._mdefs_framework._pointer.catalog_path
            relative_path = self.select_position.relative_path
            current_path = catalog_path / relative_path
            rename_path = catalog_path / user_input

            self.mdefs._mdefs_framework.rename_file_callback(current_path, rename_path)
            self._rename_window.close_window()
        except Exception as e:
            showerror(title='Yellow Pather Error 009:', message=f'{e}', parent=self.settings_window)
<<<<<<< HEAD
=======

    def select_back_sort(self):
        self.sort_count -= 1
        if self.sort_count == -1:
            self.sort_count = 3

        self.counters['sort_position'] = self.sort_count
        self.select_sort_type()

    def select_sort_type(self):
        if self.counters['sort_position'] == 0:
            self.states['sorting'] = 'disabled'
        elif self.counters['sort_position'] == 1:
            self.states['sorting'] = 'by name'
        elif self.counters['sort_position'] == 2:
            self.states['sorting'] = 'by date'
        elif self.counters['sort_position'] == 3:
            self.states['sorting'] = 'by size'
        self.sort_type = self.states['sorting']
        self.settings_gui.sorting_type.config(text=f'    {self.sort_type}    ')

        paths = self.path_manager.abs_paths
        root = self.path_manager.root_path
        path = self.path_manager.absolute_path
        reverse = True

        self.mdefs._mdefs_framework.file_sorter_callback(paths, root, path, reverse, self.sort_type)

    def select_next_sort(self):
        self.sort_count += 1
        if self.sort_count == 4:
            self.sort_count = 0

        self.counters['sort_position'] = self.sort_count
        self.select_sort_type()
>>>>>>> f38613a (Version 1.0.2)

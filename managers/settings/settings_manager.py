import tkinter as tk

from tkinter.messagebox import showerror

from functools import lru_cache
from typing import Any, Optional

class SettingsManager:
    def __init__(self, globals, callstack, settings, settings_gui) -> None:
        self.globals = globals
        self.callstack = callstack

        self.app_state = self.callstack.app_state
        self.app_render = self.callstack.app_render
        self.counters = self.globals['counters']
        self.mdefs = self.callstack.framework
        self.path_manager = self.callstack.path_manager
        self.states = self.globals['states']
        self.search = self.callstack.search_manager
        self.settings = settings
        self.settings_gui = settings_gui
        self.settings_counts = self.globals['settings_counts']
        self.select_position = self.callstack.select_position

        self.settings_window: Optional[tk.Tk] = None
        self.create_type: Any = self.states['create']
        self.sort_type: Any = self.states['sorting']
        self.type_count: int = self.settings_counts['create_position']
        self.sort_count: int = self.settings_counts['sort_position']

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
            self.states['create'] = 'Folder'
        else:
            self.states['create'] = 'File'
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

    def select_back_sort(self):
        self.sort_count -= 1
        if self.sort_count == -1:
            self.sort_count = 3

        self.counters['sort_position'] = self.sort_count
        self.select_sort_type()

    def select_sort_type(self):
        if self.counters['sort_position'] == 0:
            self.states['sorting'] = 'Standart'
        elif self.counters['sort_position'] == 1:
            self.states['sorting'] = 'By name'
        elif self.counters['sort_position'] == 2:
            self.states['sorting'] = 'By date'
        elif self.counters['sort_position'] == 3:
            self.states['sorting'] = 'By size'
        self.sort_type = self.states['sorting']
        self.settings_gui.sorting_type.config(text=f'    {self.sort_type}    ')

    def select_next_sort(self):
        self.sort_count += 1
        if self.sort_count == 4:
            self.sort_count = 0

        self.counters['sort_position'] = self.sort_count
        self.select_sort_type()

    def set_search_mode(self):
        if self.states['protect'] == 'Protected':
            self.app_state.search_protect_enabled = True
            self.settings_gui.radiobutton_1.config(fg='#0000FF')
            self.settings_gui.radiobutton_2.config(fg='#000000')
        else:
            self.app_state.search_protect_enabled = False
            self.settings_gui.radiobutton_2.config(fg='#0000FF')
            self.settings_gui.radiobutton_1.config(fg='#000000')

    def protect_on(self):
        if not self.app_state.search_protect_enabled:
            self.app_state.search_protect_enabled = True
        self.states['protect'] = 'Protected'

        self.set_search_mode()

    def protect_off(self):
        if self.app_state.search_protect_enabled:
            self.app_state.search_protect_enabled = False
        self.states['protect'] = 'Changed'

        self.set_search_mode()

    def set_insert_mode(self):
        if self.states['insert'] == 'Insert':
            self.app_state.insert_resource_name = True
            self.settings_gui.radiobutton_3.config(fg='#0000FF')
            self.settings_gui.radiobutton_4.config(fg='#000000')
        else:
            self.app_state.insert_resource_name = False
            self.settings_gui.radiobutton_4.config(fg='#0000FF')
            self.settings_gui.radiobutton_3.config(fg='#000000')

    def insert_on(self):
        if not self.app_state.insert_resource_name:
            self.app_state.insert_resource_name = True
        self.states['insert'] = 'Insert'

        self.set_insert_mode()

    def insert_off(self):
        if self.app_state.insert_resource_name:
            self.app_state.insert_resource_name = False
        self.states['insert'] = "Don't insert"

        self.set_insert_mode()

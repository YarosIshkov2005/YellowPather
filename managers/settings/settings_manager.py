import tkinter as tk

from tkinter.messagebox import showinfo, showerror

from functools import lru_cache
from typing import Optional

class SettingsManager:
    def __init__(self, settings, settings_gui, mdefs, search, app_render, select_position) -> None:
        self.settings = settings
        self.settings_gui = settings_gui
        self.mdefs = mdefs
        self.search = search
        self.app_render = app_render
        self.select_position = select_position

        self.settings_window: Optional[tk.Tk] = None
        self.create_type: str = 'catalog'
        self.type_count: int = 0

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

        self.select_create_type()

    def select_create_type(self):
        if self.type_count == 0:
            self.create_type = 'catalog'
        else:
            self.create_type = 'file'
        self.settings_gui.select_type.config(text=f'    {self.create_type}    ')

    def next_type(self):
        self.type_count += 1
        if self.type_count == 2:
            self.type_count = 0

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

import tkinter as tk

from tkinter.messagebox import showinfo, showerror

from functools import lru_cache
from typing import Optional

class SettingsManager:
    def __init__(self, settings, settings_gui, mdefs, search, app_render) -> None:
        self.settings = settings
        self.settings_gui = settings_gui
        self.mdefs = mdefs
        self.search = search
        self.app_render = app_render

        self.settings_window: Optional[tk.Tk] = None
        self.create_type: str = 'catalog'
        self.type_count: int = 0

        self._rename_window = self.rename_window
        self._rename_window.callback_function = self.create_new_resource

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

    def create_rename_window(self):
        self._rename_window.create_window()

    def create_new_resource(self, new_path: str = ''):
        try:
            self.mdefs._mdefs_framework.bootstrap(new_path, self.create_type)
            self._rename_window.close_window()
        except Exception as e:
            showerror(title='Yellow Pather Error 009:', message=f'{e}', parent=self.settings_window)

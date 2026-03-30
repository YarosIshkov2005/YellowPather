import os

import tkinter as tk

from pathlib import Path

class InsertManager:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.app_gui = self.callstack.app_gui
        self.counters = self.globals['insert']

    def reset_positions(self):
        self.counters['root_position'] = 0
        self.counters['start_position'] = 0

    def set_positions(self):
        self.counters['root_position'] = self.app_gui.path_entry.index(tk.INSERT)
        self.counters['start_position'] = self.app_gui.path_entry.index(tk.INSERT)

    def insert_path(self, input_path: str, index: int, add_slash: bool = True):
        input_path = str(input_path) if isinstance(input_path, Path) else input_path
        slash = ''

        if add_slash:
            slash = os.sep

        self.app_gui.path_entry.delete(index, tk.END)
        self.app_gui.path_entry.insert(index, input_path + slash)

    def clear_path(self):
        self.app_gui.path_entry.delete(self.counters['start_position'], tk.END)
        self.app_gui.path_entry.focus()

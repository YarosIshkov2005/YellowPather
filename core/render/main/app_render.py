import os

import tkinter as tk

from pathlib import Path
from typing import Callable

class AppRenderCore:
    def __init__(self, globals, callstack):
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.button_state = self.callstack.button_state
        self.counters = self.globals['insert']
        self.path_manager = self.callstack.path_manager
        self.states = self.globals['states']
        self.select_state = self.callstack.select_state
        self.select_position = self.callstack.select_position

        self.callback: Callable = None

    def protect_root_delete(self, event=None) -> None:
        """
        Protects root path from deletion in entry field.

        Args:
            event: Key event (optional).

        Returns:
            'break' if deletion in protected area, else None.
        """
        current_position = self.app_gui.path_entry.index(tk.INSERT)
        if (current_position <= self.counters['root_position'] 
            and event.keysym in ['BackSpace', 'Delete']):
            return 'break'

    def protect_root_path(self, event=None) -> None:
        """
        Prevents cursor movement into root path protected area.

        Args:
            event: Mouse event (optional).
        """
        current_position = self.app_gui.path_entry.index(tk.INSERT)
        if current_position <= self.counters['root_position']:
            self.app_gui.path_entry.selection_clear()
            self.app_gui.path_entry.icursor(tk.END)

    def update_select_window(self) -> None:
        """Updates Listbox content with current directory items."""
        self.protect_root_path()

        if not self.app_state.is_recursive_search:
            self.callback(self.path_manager.abs_paths, 
                self.path_manager.root_path, self.path_manager.resource_path, 
                    True, self.states['sorting'])

        self.app_gui.select_window.delete(0, tk.END)
        self.app_gui.select_window.insert(0, *self.path_manager.short_names)

    def canonize_entered_path(self, input_path: Path = None) -> None:
        """Normalizes entered path relative to root."""
        canonize_path = (Path(input_path) 
            if isinstance(input_path, str) else input_path)
        path_parts = canonize_path.parts
        navigation_path = Path('')

        for part in path_parts:
            navigation_path /= part

        navigation_path = str(navigation_path)
        if navigation_path == '.':
            navigation_path = ''

        self.app_gui.path_entry.delete(self.counters['root_position'], tk.END)
        self.app_gui.path_entry.insert(self.counters['root_position'], navigation_path)
        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        if str(canonize_path) == '.':
            return

        root_path = self.path_manager.root_path
        absolute_path = root_path / navigation_path

        if absolute_path.is_dir():
            self.add_slash(absolute_path)

    def add_slash(self, current_path: str) -> None:
        """Adds trailing slash to directory paths."""
        target_path = Path(current_path) if isinstance(current_path, str) else current_path

        if target_path.is_file():
            return

        if self.path_manager.input_path.endswith(os.sep):
            return

        self.app_gui.path_entry.insert(tk.END, os.sep)
        self.app_gui.path_entry.xview_moveto(1.0)

    def safe_popup_truncate(self, name: str, max_length=25) -> str:
        """
        Truncates long names for display in popup messages.

        Args:
            name: Name to truncate.
            max_length: Maximum length before truncation.

        Returns:
            Truncated name with ellipsis if needed.
        """
        str_name = str(name) if isinstance(name, Path) else name

        if len(str_name) <= max_length:
            return str_name

        min_visible = 10
        truncate_at = max(min_visible, max_length - 3)
        return str_name[:truncate_at] + '...'

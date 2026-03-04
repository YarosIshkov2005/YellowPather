import os

import tkinter as tk

from pathlib import Path

class AppRenderCore:
    def __init__(self, root, counters, app_gui, app_state, select_position, select_state, button_state, path_manager):
        self.root = root
        self.counters = counters
        self.app_gui = app_gui
        self.app_state = app_state
        self.select_position = select_position
        self.select_state = select_state
        self.button_state = button_state
        self.path_manager = path_manager

        self.index: int = 0
        self.elements_count: int = 0
        self.current_index: int = 1

    def protect_root_delete(self, event=None) -> None:
        """
        Protects root path from deletion in entry field.

        Args:
            event: Key event (optional).

        Returns:
            'break' if deletion in protected area, else None.
        """
        current_position = self.app_gui.path_entry.index(tk.INSERT)
        if (current_position <= self.counters['root_position'] and event.keysym in ['BackSpace', 'Delete']):
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

        self.app_gui.select_window.delete(0, tk.END)
        self.app_gui.select_window.insert(0, *self.path_manager.short_names)

        if self.update_position():
            return

        self.app_gui.select_button.config(text='Select')
        self.app_gui.select_window.config(selectbackground='blue')
        
        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        self.button_state.control_update_button()
        self.button_state.control_up_button()
        self.button_state.control_select_button()
        self.button_state.control_down_button()

        self.button_state.control_back_button()
        self.button_state.control_next_button()
        self.button_state.control_settings_button()
        self.button_state.update_search_state()

        self.element_count()

    def update_position(self):
        if len(self.path_manager.short_names) >= 1:
            self.app_gui.select_window.see(self.index)
            self.app_gui.select_window.selection_set(self.index)

            self.select_position.selected_index = self.index
            self.select_position.select_position()

            self.path_manager.current_path = self.select_position.absolute_path

            if self.app_state.block_when_update:
                self.app_state.block_when_update = False
                return True
            return False

    def element_count(self):
        if (self.app_state.reset_button_active or 
            self.app_state.next_button_active):
            self.current_index = 1
        elif self.app_state.back_button_active:
            self.current_index = self.select_state.current_position + 1

        self.elements_count = len(self.path_manager.short_names)
        if self.elements_count == 0:
            self.current_index = 0
            
        self.app_gui.elements_label.config(text=f'Elements: {self.elements_count}')
        self.app_gui.current_label.config(
            text=f'Element: {self.current_index}/{self.elements_count}')

        if self.app_state.reset_button_active:
            self.app_state.reset_button_active = False
        elif self.app_state.back_button_active:
            self.app_state.back_button_active = False
        elif self.app_state.next_button_active:
            self.app_state.next_button_active = False

    def insert_root_path(self) -> None:
        """Inserts root path into entry field."""
        if self.app_state.root_path_inserted:
            return

        str_root_path = str(self.path_manager.root_path)

        navigation_path = ''
        if str_root_path == '/' or str_root_path.endswith(os.sep):
            navigation_path = str(self.path_manager.root_path)
        else:
            navigation_path = str(self.path_manager.root_path)
            
        self.app_gui.select_window.see(self.index)
        self.app_gui.select_window.selection_set(self.index)

        self.app_gui.path_entry.insert(0, navigation_path)
        self.app_gui.path_entry.focus()

        self.add_slash(navigation_path)

        self.counters['root_position'] = self.app_gui.path_entry.index(tk.INSERT)
        self.counters['start_position'] = self.app_gui.path_entry.index(tk.INSERT)

        self.select_state.current_select()
        self.select_state.add_next_point()

        if not self.app_state.root_path_inserted:
            self.app_state.root_path_inserted = True

        self.path_manager.current_path = self.path_manager.absolute_path

    def canonize_entered_path(self, canonize_path: Path) -> None:
        """Normalizes entered path relative to root."""
        parts_path = canonize_path.parts
        parent_path = self.path_manager.root_path

        for part in parts_path:
            parent_path /= part

        relative_path = parent_path.relative_to(self.path_manager.root_path)
        resources = len(self.path_manager.short_names)
        if resources >= 1:
            navigation_path = relative_path / self.select_position.relative_path
        else:
            navigation_path = relative_path

        self.app_gui.path_entry.delete(self.counters['root_position'], tk.END)
        self.app_gui.path_entry.insert(self.counters['root_position'], navigation_path)
        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        root_path = self.path_manager.root_path
        absolute_path = root_path / navigation_path
        self.path_manager.input_path = absolute_path

        if absolute_path.is_dir():
            self.add_slash(navigation_path)

    def add_slash(self, current_path: str) -> None:
        """Adds trailing slash to directory paths."""
        target_path = Path(current_path) if isinstance(current_path, str) else current_path

        if target_path.is_file():
            return

        if str(self.path_manager.input_path).endswith(os.sep):
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
        if len(name) <= max_length:
            return name

        min_visible = 10
        truncate_at = max(min_visible, max_length - 3)
        return name[:truncate_at] + '...'

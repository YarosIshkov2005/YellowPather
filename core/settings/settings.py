import tkinter as tk

from tkinter.messagebox import showerror

from pathlib import Path
from functools import lru_cache
from typing import Optional

class SettingsCore:
    """
    Application settings management class.

    Handles settings window creation, file operations, and
    extension-based file type detection.
    """

    def __init__(self, globals, callstack) -> None:
        """
        Initializes FileManagerSettings.

        Args:
            root (tk.Tk): Main Tkinter window.
            app_gui: Program GUI.
            app_state: Program state.
            path_manager: Paths for the program.
        """
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.app_render = self.callstack.app_render
        self.button_state = self.callstack.button_state
        self.counters = self.globals['counters']
        self.mdefs = self.callstack.framework
        self.path_manager = self.callstack.path_manager
        self.states = self.globals['states']
        self.search = self.callstack.search_manager
        self.select_position = self.callstack.select_position
        
        self.settings_window: Optional[tk.Tk] = None

        self._settings_gui = self.settings_gui
        self._settings_events = self.settings_events
        self._settings_manager = self.settings_manager
        self.open_file_callback = None

    @property
    @lru_cache(maxsize=None)
    def settings_gui(self):
        from core.gui.settings.settings_gui import SettingsGUI
        return SettingsGUI(settings=self)

    @property
    @lru_cache(maxsize=None)
    def settings_events(self):
        from core.events.settings.settings_events import SettingsEvents
        return SettingsEvents(settings=self, settings_gui=self._settings_gui)

    @property
    @lru_cache(maxsize=None)
    def settings_manager(self):
        from managers.settings.settings_manager import SettingsManager
        return SettingsManager(globals=self.globals, callstack=self.callstack,
             settings=self, settings_gui=self._settings_gui)

    def create_window(self) -> None:
        """Creates settings window."""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title('Settings')
        self.settings_window.resizable(False, False)
        self.settings_window.grab_set()
        self.settings_window.protocol('WM_DELETE_WINDOW', self.close_window)

        self._settings_gui.settings_window = self.settings_window
        self._settings_manager.settings_window = self.settings_window
        self._settings_gui.widgets_container()
        self._settings_gui.create_widgets()

        self._settings_events.bind_events()

        self._settings_manager.set_search_mode()
        self._settings_manager.set_insert_mode()
        
        self.mdefs._mdefs_framework.callbacks['settings'] = self.settings_window
        self.control_open_button()
        self.button_state.control_create_button(self._settings_gui)

    def control_open_button(self) -> None:
        """Controls open button state based on selection."""
        select_path = (Path(self.path_manager.selected_path) if isinstance(
            self.path_manager.selected_path, str) else self.path_manager.selected_path)

        if select_path is None:
            self._settings_gui.open_button.config(state='disabled')
            self._settings_gui.create_button.config(state='normal')
            return

        if select_path.is_file():
            self._settings_gui.open_button.config(state='normal')
            self._settings_gui.create_button.config(state='disabled')
        else:
            self._settings_gui.open_button.config(state='disabled')
            self._settings_gui.create_button.config(state='normal')

    def show_error(self) -> None:
        """Shows module not found error."""
        showerror(
            title='Yellow Pather Error 015:',
            message='Module Error: The operation was canceled. The module was not found',
            parent=self.root
        )

    def close_window(self) -> None:
        """Closes settings window."""
        if self.settings_window:
            self.settings_window.grab_release()
            self.settings_window.destroy()
            self.settings_window = None

        if self.root and self.root.winfo_exists():
            self.root.lift()
            self.root.focus_force()
            self.app_gui.path_entry.focus()

        path = self.path_manager.absolute_path
        self.app_render.update_select_window()
        self.app_render.canonize_entered_path(path)

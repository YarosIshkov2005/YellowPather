import string

import tkinter as tk

from tkinter.messagebox import showerror

from typing import Callable, Dict, Optional

class RenameWindow:
    def __init__(self, root) -> None:
        self.root = root

        self.rename_window: Optional[tk.Tk] = None

        self.callbacks: Dict[Callable] = {}

        self.target: str = 'rename'
        self.forbidden: str = '\\ / : * ? " < > |'

    def create_window(self):
        if self.rename_window and self.rename_window.winfo_exists():
            self.rename_window.lift()
            return

        self.rename_window = tk.Toplevel(self.root)
        self.rename_window.title('Enter Name')
        self.rename_window.resizable(False, False)
        self.rename_window.grab_set()
        self.rename_window.protocol('WM_DELETE_WINDOW', self.close_window)

        self._rename_gui = self.rename_gui
        self._rename_gui.widgets_container()
        self._rename_gui.create_widgets()
        self._rename_gui.enter_field.focus()

        self._rename_events = self.rename_events
        self._rename_events.bind_events()

    @property
    def rename_gui(self):
        from core.gui.rename.rename_gui import RenameGUI
        return RenameGUI(rename_window=self.rename_window)

    @property
    def rename_events(self):
        from core.events.rename.rename_events import RenameEvents
        return RenameEvents(rename=self, rename_gui=self._rename_gui)

    def check_length_string(self, user_input):
        string_length = len(user_input)
        if string_length == 0:
            showerror(
                title='Yellow Pather Error 016:',
                message=f'Input Error: The string cannot be empty (current length: {string_length})',
                parent=self.rename_window
            )
            self._rename_gui.enter_field.focus()
            return False
        return True

    def check_forbidden_symbols(self, user_input):
        punctuation = string.punctuation
        parts = [part for part in user_input if part in punctuation]
        if all(part for part in parts if part in self.forbidden) and parts:
            showerror(
                title='YellowPather Error 021:',
                message=f"Characters {self.forbidden} not supported!",
                parent=self.rename_window
            )
            self._rename_gui.enter_field.focus()
            return False
        return True

    def target_function_callback(self):
        user_input = self._rename_gui.enter_field.get()
        if not self.check_length_string(user_input):
            return

        if not self.check_forbidden_symbols(user_input):
            return

        if self.target == 'create':
            self.callbacks['create'](user_input)
        else:
            self.callbacks['rename'](user_input)

    def close_window(self):
        if self.rename_window:
            self.rename_window.grab_release()
            self.rename_window.destroy()
            self.rename_window = None

        if self.root and self.root.winfo_exists():
            self.root.lift()
            self.root.focus_force()

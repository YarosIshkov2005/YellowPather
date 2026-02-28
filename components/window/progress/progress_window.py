import tkinter as tk

class ProgressWindow:
    def __init__(self, root, app_gui, app_state) -> None:
        self.root = root
        self.app_gui = app_gui
        self.app_state = app_state

        self.progress_window: tk.Tk = None

    @property
    def progress_gui(self):
        from core.gui.progress.progress_gui import ProgressGUI
        return ProgressGUI(progress_window=self.progress_window)

    @property
    def progress_events(self):
        from core.events.progress.progress_events import ProgressEvents
        return ProgressEvents(progress_window=self, progress_gui=self._progress_gui)

    def create_window(self):
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.resizable(False, False)
        self.progress_window.grab_set()
        self.progress_window.protocol('WM_DELETE_WINDOW', self.close_window)

        self._progress_gui = self.progress_gui
        self._progress_gui.widgets_container()
        self._progress_gui.create_widgets()

        self._progress_events = self.progress_events
        self._progress_events.bind_events()

    def window(self, name: str):
        self.progress_window.title(name)

    def description(self, text: str):
        self._progress_gui.description_label.config(text=text)

    def progress(self, command: str):
        self._progress_gui.progress_bar.start() if command == 'start' else self._progress_gui.progress_bar.stop()

    def length(self, length: int):
        self._progress_gui.progress_bar.config(length=length)

    def mode(self, mode: str):
        self._progress_gui.progress_bar.config(mode=mode)

    def process(self, text: str):
        if self._progress_gui.progress_label.winfo_exists():
            self._progress_gui.progress_label.config(text=text)

    def cancel_operation(self):
        if not self.app_state.is_operation_canceled:
            self.app_state.is_operation_canceled = True
            
        self._progress_gui.progress_bar.stop()
        self.app_gui.path_entry.focus()
        self.close_window()

    def close(self):
        self.close_window()

    def close_window(self):
        if self.progress_window:
            self.progress_window.grab_release()
            self.progress_window.destroy()
            self.progress_window = None

        if self.root and self.root.winfo_exists():
            self.root.lift()
            self.root.focus_force()
            self.app_gui.path_entry.focus()

import os

from tkinter.messagebox import showinfo, showerror
from pathlib import Path

class RenameFile:
    def __init__(self, app_render, daemon, path_manager, search, select_state, callbacks) -> None:
        self.app_render = app_render
        self.daemon = daemon
        self.path_manager = path_manager
        self.search = search
        self.select_state = select_state
        self.callbacks = callbacks

    def rename_file(self, current_path: Path, rename_path: Path):
        try:
            self.daemon.window_focus()

            os.rename(str(current_path), str(rename_path))

            showinfo(
                title='Message:',
                message=f"Renamed '{current_path.name}' to '{rename_path.name}'",
                parent=self.daemon.notification_window
            )
            self.daemon.notification_window.protocol(
                'WM_DELETE_WINDOW', self.daemon.return_focus(
                    self.callbacks['settings']))
        except Exception as e:
            showerror(title='Yellow Pather Error 009:', message=f'{e}', parent=self.daemon.notification_window)

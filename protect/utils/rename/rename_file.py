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

            self.path_manager.absolute_path = rename_path.parent
            self.path_manager.current_path = rename_path

            self.search.add_paths()

            self.app_render.index = self.select_state.index_list[-1]
            self.app_render.update_select_window()
            self.app_render.canonize_entered_path(rename_path.parent)
        except Exception as e:
            showerror(title='Yellow Pather Error 009:', message=f'{e}', parent=self.daemon.notification_window)

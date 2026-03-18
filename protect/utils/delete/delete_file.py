import shutil

from tkinter.messagebox import askyesno, showinfo, showerror

from pathlib import Path

class DeleteFile:
    def __init__(self, app_perms, app_render, daemon, pointer, path_manager, search, select_state, select_position, callbacks) -> None:
        self.app_perms = app_perms
        self.app_render = app_render
        self.daemon = daemon
        self.pointer = pointer
        self.path_manager = path_manager
        self.search = search
        self.select_state = select_state
        self.select_position = select_position
        self.callbacks = callbacks

    def delete_file(self, delete_path: Path):
        length = 0
        short_name = self.app_render.safe_popup_truncate(delete_path)
        if self.select_position.absolute_path.is_dir():
            resources = [path for path in self.select_position.absolute_path.iterdir()]
            length = len(resources)
            warning_message = (
                f"Do you really want to delete '{short_name}' permanently ({length})?\n\n"
                'Continue?'
            )
        else:
            warning_message = (
                f"Do you really want to delete '{short_name}' permanently?\n\n"
                'Continue?'
            )
        try:
            self.daemon.window_focus()

            if not self.app_perms.check_perms(delete_path):
                self.daemon.notification_window.protocol(
                    'WM_DELETE_WINDOW', self.daemon.return_focus(
                        self.callbacks['settings']))
                return

            if delete_path.is_symlink():
                showerror(
                    title='Yellow Pather Error 010:',
                    message='You cannot delete a symlink',
                    parent=self.daemon.notification_window
                )
                self.daemon.notification_window.protocol(
                    'WM_DELETE_WINDOW', self.daemon.return_focus(
                        self.callbacks['settings']))
                return

            result = askyesno(
                title='Warning:', 
                message=warning_message, 
                parent=self.daemon.notification_window
            )
            self.daemon.notification_window.protocol(
                'WM_DELETE_WINDOW', self.daemon.return_focus(
                    self.callbacks['settings']))
            if not result:
                return

            if delete_path.is_dir():
                shutil.rmtree(delete_path)
            elif delete_path.is_file():
                delete_path.unlink(missing_ok=True)

            showinfo(
                title='Message:',
                message=f"'{delete_path.name}' was deleted",
                parent=self.daemon.notification_window
            )
            self.daemon.notification_window.protocol(
                'WM_DELETE_WINDOW', self.daemon.return_focus(
                    self.callbacks['settings']))

            self.path_manager.absolute_path = self.pointer.catalog_path

            self.search.add_paths()

            self.select_state.current_position = self.app_render.index
            self.select_state.pop_back_point()
            self.select_state.current_select()
            self.select_state.add_next_point()

            self.app_render.current_index = self.app_render.index + 1
            self.app_render.update_select_window()

            current_path = self.path_manager.current_path.parent
            self.app_render.canonize_entered_path(current_path)
        except Exception as e:
            showerror(
                title='Yellow Pather Error 022:', 
                message=f'{e}', 
                parent=self.daemon.notification_window
            )

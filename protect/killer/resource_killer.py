import shutil

from tkinter.messagebox import showinfo, showwarning, showerror

from pathlib import Path

class ResourceKiller:
    def __init__(self, app_perms, app_render, daemon, path_manager, search, settings_window) -> None:
        self.app_perms = app_perms
        self.app_render = app_render
        self.daemon = daemon
        self.path_manager = path_manager
        self.search = search
        self.settings_window = settings_window

    def resource_killer(self, resource: Path):
        warning_message = (
            f"Do you really want to delete '{resource.name}' permanently?\n\n"
            'Continue?'
        )
        try:
            self.daemon.window_focus()

            if not self.app_perms.check_permission(resource):
                self.daemon.notification_window.protocol(
                    'WM_DELETE_WINDOW', self.daemon.return_focus(
                        self.settings_window)
                )
                return

            result = showwarning(
                title='Message:', 
                message=warning_message, 
                parent=self.daemon.notification_window
            )
            self.daemon.notification_window.protocol(
                'WM_DELETE_WINDOW', self.daemon.return_focus(
                    self.settings_window)
            )
            if not result:
                return

            if resource.is_dir():
                shutil.rmtree(resource)
            elif resource.is_file():
                resource.unlink(missing_ok=True)

            showinfo(
                title='Message:',
                message=f"'{resource.name}' was deleted",
                parent=self.daemon.notification_window
            )
            self.daemon.notification_window.protocol(
                'WM_DELETE_WINDOW', self.daemon.return_focus(
                    self.settings_window)
            )

            self.path_manager.absolute_path = self.path_manager.root_path
            self.path_manager.current_path = None

            self.search.add_paths()

            self.app_render.update_select_window()
        except Exception as e:
            showerror(
                title='Yellow Pather Error 022:', 
                message=f'{e}', 
                parent=self.daemon.notification_window
            )

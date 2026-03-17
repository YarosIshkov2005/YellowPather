from tkinter.messagebox import showinfo, showerror

from pathlib import Path
from typing import List

class Bootstrapper:
    def __init__(self, root, notification_window, pointer, path_manager, callbacks, search, select_state, app_render) -> None:
        self.root = root
        self.notification_window = notification_window
        self.pointer = pointer
        self.path_manager = path_manager
        self.callbacks = callbacks
        self.search = search
        self.select_state = select_state
        self.app_render = app_render

        self.paths: List[Path] = []
        
    def bootstrapper(self, input_path: str, create_path: Path, create_type: str) -> None:
        self.notification_window.window_focus()
        short_names = [path.name for path in self.path_manager.abs_paths]
        if input_path in short_names:
            showerror(
                title='Yellow Pather Error 009:',
                message=f"Exist Error: {create_type} named '{input_path}' already exists",
                parent=self.notification_window.notification_window
            )
            self.notification_window.notification_window.protocol(
                'WM_DELETE_WINDOW', self.notification_window.return_focus(
                    self.callbacks['settings']))
            return

        extension = '.' + str(create_path).split('.')[-1]
        extensions = self.callbacks['extensions']

        languages = extensions['languages'].keys()
        text = extensions['text'].keys()
        others = extensions['others'].keys()

        if create_type == 'folder':
            if (extension in languages or extension in text 
                or extension in others):
                showerror(
                    title='Yellow Pather Error 009:',
                    message=f"You cannot create a {create_type} with the extension '{extension}'",
                    parent=self.notification_window.notification_window
                )
                self.notification_window.notification_window.protocol(
                    'WM_DELETE_WINDOW', self.notification_window.return_focus(
                        self.callbacks['settings']))
                return

        if create_type == 'folder':
            create_path.mkdir(exist_ok=True, parents=True)
        else:
            create_path.touch()

        self.path_manager.absolute_path = self.pointer.catalog_path
        self.path_manager.current_path = None

        self.app_render.update_select_window()

        showinfo(
            title='Message:', 
            message=f"New {create_type}: '{create_path.name}' was created!", 
            parent=self.notification_window.notification_window
        )
        self.notification_window.notification_window.protocol(
            'WM_DELETE_WINDOW', self.notification_window.return_focus(
                self.callbacks['settings']))

        if len(short_names) == 0:
            self.select_state.index_list.append(0)

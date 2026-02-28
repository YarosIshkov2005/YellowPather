import os
import platform

from tkinter.messagebox import askyesno

from typing import Optional
from pathlib import Path

class AccessManager:
    def __init__(self, root, progress_window, app_state, callbacks, path_iterator) -> None:
        self.root = root
        self.progress_window = progress_window
        self.app_state = app_state
        self.callbacks = callbacks
        self.path_iterator = path_iterator

        self.input_path: Optional[Path] = None

    def access(self, check_path: Path):
        input_path = Path(check_path) if isinstance(check_path, str) else check_path
        self.input_path = input_path
        
        if not self.is_path_symlink(input_path):
            warning = (
                'Before analyzing the entered path, YellowPather will check all paths in the system.\n\n'
                'Are you sure you want to continue?'
            )
            result = askyesno(title='Warning', message=warning, parent=self.root)
            if not result:
                return

            if not self.start_search():
                return

    def is_path_symlink(self, check_path: Path):
        return check_path.is_symlink()

    def start_search(self):
        root_path = ''
        system = platform.system()

        if system == 'Windows':
            root_path = 'C:\\'
        elif ['Darwin', 'Linux']:
            root_path = '/'

            if system == 'Linux' and 'ANDROID_STORAGE' in os.environ.keys():
                if os.getuid() == 0:
                    root_path = '/'
                else:
                    root_path = '/storage/emulated/0/'
                system = 'Android'

        self.progress_window.create_window()
        
        progress_window_name = 'Searching'
        self.callbacks['window'](progress_window_name)

        process_description = (
            f'YellowPather checks all paths in the {system}.\n\n'
            'The operation may take a long time, please be patient.'
        )
        self.callbacks['description'](process_description)

        progress_bar_length = 370
        self.callbacks['length'](progress_bar_length)

        progress_bar_mode = 'indeterminate'
        self.callbacks['mode'](progress_bar_mode)

        process_message = 'Processed: 0 files'
        self.callbacks['process'](process_message)

        self.path_iterator.start_iteration(root_path)
        if self.app_state.is_operation_canceled:
            self.app_state.is_operation_canceled = False
            return False
        return True

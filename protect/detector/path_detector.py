import queue
import threading

from typing import List
from pathlib import Path

class PathDetector:
    def __init__(self, root, app_state, access_manager, paths_dict) -> None:
        self.root = root
        self.app_state = app_state
        self.access_manager = access_manager
        self.paths_dict = paths_dict

        self.queue = queue.Queue()

        self.root.after(100, self.poll_queue)

    def poll_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg is None:
                    self.access_manager.callbacks['close']()
                    return
                if isinstance(msg, tuple) and msg[0] == 'count':
                    self.access_manager.callbacks['process'](f'Processed: {msg[1]} files')
                self.root.update_idletasks()
        except queue.Empty:
            pass
        finally:
            self.root.after(50, self.poll_queue)

    def iteration(self):
        if self.app_state.is_operation_canceled:
            return

        symlinks = self.paths_dict['symlinks']
        input_path = self.access_manager.input_path

        process_description = (
            f'YellowPather checks {self.access_manager.input_path} for a symlink.\n\n'
            'The operation may take a long time, please be patient.'
        )
        self.access_manager.callbacks['description'](process_description)

        process_message = 'Processed: 0 files'
        self.access_manager.callbacks['process'](process_message)

        self.start_iteration(input_path, symlinks)

    def start_iteration(self, input_path: Path, symlinks: List):
        threading.Thread(target=self.iteration_paths, args=(input_path, symlinks), daemon=True).start()

    def iteration_paths(self, input_path: Path, symlinks: List):
        try:
            count = 0
            self.access_manager.callbacks['progress']('start')
            for path in symlinks:
                if self.app_state.is_operation_canceled:
                    self.queue.put(None)
                    return
                if input_path.samefile(path):
                    self.queue.put(None)
                    return
                count += 1
                if count % 10 == 0:
                    self.queue.put(('count', count))
            self.access_manager.callbacks['progress']('stop')
        except Exception as e:
            self.queue.put(f'Error: {e}')
        finally:
            self.queue.put(None)

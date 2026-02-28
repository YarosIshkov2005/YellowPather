import os
import queue
import threading

from pathlib import Path

class PathIterator:
    def __init__(self, root, progress_window, app_state, callbacks, paths_dict) -> None:
        self.root = root
        self.progress_window = progress_window
        self.app_state = app_state
        self.callbacks = callbacks
        self.paths_dict = paths_dict

        self.queue = queue.Queue()

        self.root.after(100, self.poll_queue)

    def poll_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg is None:
                    self.callbacks['finish']()
                    return
                if isinstance(msg, tuple) and msg[0] == 'count':
                    self.callbacks['process'](f'Processed: {msg[1]} files')
                self.root.update_idletasks()
        except queue.Empty:
            pass
        finally:
            self.root.after(50, self.poll_queue)

    def start_iteration(self, root_path: str):
        threading.Thread(target=self.iteration, args=(root_path,), daemon=True).start()

    def iteration(self, root_path: str):
        try:
            count = 0
            self.callbacks['progress']('start')
            for dirname, _, filenames in os.walk(root_path):
                for filename in filenames:
                    if self.app_state.is_operation_canceled:
                        self.queue.put(None)
                        return
                    path = Path(dirname) / filename
                    if path.is_symlink():
                        self.paths_dict['symlinks'].append(path)
                    else:
                        self.paths_dict['paths'].append(path)
                    count += 1
                    if count % 10 == 0:
                        self.queue.put(('count', count))
            self.callbacks['progress']('stop')
        except Exception as e:
            self.queue.put(f'Error: {e}')
        finally:
            self.queue.put(None)
    
import os
import json
import platform

from tkinter.messagebox import showerror

from pathlib import Path

class SystemDetector:
    """Calculates the current operating system on the device."""
    def __init__(self, globals) -> None:
        self.globals = globals

        self.root = self.globals['root']
        self.system_paths = self.globals['system_paths']

        self.SYSTEM_NAME: dict[str] = {
            'Windows': 'Windows',
            'Darwin': 'MacOS',
            'Linux': 'Linux'
        }

    def get_system(self):
        """Returns the kernel and the operating system name."""
        system = platform.system()
        system_name = self.SYSTEM_NAME[system]
        return system, system_name

    def get_system_config(self):
        system_tuple = self.get_system()
        system_name = system_tuple[1]
        system_config = {}

        with open(self.system_paths, 'r', encoding='utf-8') as file:
            data = file.read()
            system_config = json.loads(data)

        system = system_tuple[0]
        if system not in system_config.keys():
            showerror(title='Yellow Pather Error 017:', message=f'Unknown system {system}', parent=self.root)
            self.close_window()
            return {}

        if system == 'Linux' and 'ANDROID_STORAGE' in os.environ.keys():
            system = 'Android'
            system_name = system

        current_system = system_config.get(system)
        if current_system is None:
            showerror(title='Yellow Pather Error 017:', message=f'System {system_name} not configured', parent=self.root)
            self.close_window()
            return {}

        root_path = current_system.get('root')
        if root_path is None:
            showerror(title='Yellow Pather Error 017:', message=f'Root path not set for {system_name}', parent=self.root)
            self.close_window()
            return {}

        if root_path not in current_system.values():
            showerror(title='Yellow Pather Error 017:', message=f'Root path not found for {system_name}', parent=self.root)
            self.close_window()
            return {}

        auto_detect = system_config.get('auto_detect')
        candidate_path = Path(root_path)

        return {
            'system_config': system_config,
            'auto_detect': auto_detect,
            'root_path': root_path,
            'candidate_path': candidate_path
        }

    def close_window(self) -> None:
        """Closes application and all additional windows."""
        if self.root and self.root.winfo_exists():
            self.root.destroy()

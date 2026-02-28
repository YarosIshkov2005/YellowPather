from tkinter.messagebox import askyesno, showinfo, showerror

from pathlib import Path
from typing import Optional

class SystemManager:
    def __init__(self, root, settings, app_gui, app_state, app_perms, secure_state, system_paths, os_system, path_manager, secure_manager) -> None:
        self.root = root
        self.settings = settings
        self.app_gui = app_gui
        self.app_state = app_state
        self.app_perms = app_perms
        self.secure_state = secure_state
        self.system_paths = system_paths
        self.os_system = os_system
        self.path_manager = path_manager
        self.secure_manager = secure_manager

        self.root_path: Optional[Path] = None
        self.user_id: str = '0'

    def check_root_path(self) -> bool:
        """
        Detects and sets root path from configuration.

        Returns:
            True if root path is successfully detected.
        """
        root_config = self.os_system.get_system_config()
        system_config = root_config.get('system_config')
        auto_detect = root_config.get('auto_detect')
        root_path = root_config.get('root_path')
        candidate_path = root_config.get('candidate_path')

        if not self.secure_state.hide_storage_error:
            self.secure_state.hide_storage_error = True

        if not auto_detect:
            if not self.set_root_path(system_config, root_path, candidate_path):
                return {}

            return {
                'root_path': self.root_path
            }

        if not self.app_perms.check_permission(candidate_path):
            return {}

        if not self.check_perms(root_path, candidate_path):
            return {}

        self.root_path = candidate_path
        return {
            'root_path': self.root_path
        }

    def set_root_path(self, system_config: dict, root_path: str, candidate_path: Path):
        is_root_path = system_config.get('root_path')
        is_user_path = system_config.get('user_path')
        is_device_path = system_config.get('device_path')

        if (is_root_path and is_user_path and is_device_path) or (is_root_path and is_user_path) or (is_user_path and is_device_path) or (is_root_path and is_device_path):
            error_msg = (
                f"Disable one of the options:\n\n"
                f"root_path {is_root_path} -> {not is_root_path}"
                f" or user_path {is_user_path} -> "
                f"{not is_user_path}"
                f" or device_path {is_device_path} -> "
                f"{not is_device_path} \n\n"
                f"--> in YellowPather -> YellowPather -> config -> {self.system_paths.name}"
            )
            showinfo(title='Yellow Pather Error 012:', message=error_msg, parent=self.root)
            self.root_path = 'system'

            self.app_gui.back_button.config(state='disabled')
            self.app_gui.next_button.config(state='disabled')
            self.app_gui.path_entry.focus()

            if not self.app_state.manual_input_mode:
                self.app_state.manual_input_mode = True
                return True

        elif is_root_path:
            if not self.app_perms.check_permission(candidate_path):
                self.root_path = 'system'
                return False

            if not self.check_perms(root_path, candidate_path):
                self.root_path = 'system'
                return False

            self.root_path = candidate_path
            return True

        elif is_user_path:
            self.root_path = Path(__file__).parents[2] / 'users' / self.user_id
            self.create_user_catalog(self.root_path)

            if not self.app_state.resolve_work_main:
                self.app_state.resolve_work_main = True
            return True

        elif is_device_path:
            self.root_path = Path(__file__).parents[4]
            return True

        else:
            self.root_path = Path.cwd() / 'users' / self.user_id
            self.create_user_catalog(self.root_path)

            if not self.app_state.resolve_work_main:
                self.app_state.resolve_work_main = True
            return True
        return False

    def check_perms(self, root_path: str, candidate_path: str):
        if self.secure_manager.check_input_path(
            input_path=root_path, 
            root_path=candidate_path, 
            check_path=candidate_path
        ):
            return True

        error_msg = (
            f"Permission Error: Yellow Pather root 1 '{root_path}'\n\n"
            "Reason: Insufficient permissions to open the system storage\n\n"
            "A input mode will be actived. Do you want to continue?"
        )

        result = askyesno(
            title='Yellow Pather Error 011:',
            message=error_msg,
            parent=self.root
        )

        if not result:
            self.close_window()
            return False
        return False

    def close_window(self) -> None:
        """Closes application and all additional windows."""
        self.settings.close_window()

        if self.root and self.root.winfo_exists():
            self.root.destroy()

    def create_user_catalog(self, root_path):
        """Creates catalog for user."""
        try:
            root_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            showerror(title='Yellow Pather Error 007:', message=f'Create Error: {e}', parent=self.root)

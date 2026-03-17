# Standard libraries
import json
import os
import subprocess

# Third-party libraries
import tkinter as tk
from tkinter.messagebox import showinfo, showerror

# Local modules
from functools import wraps, lru_cache
from pathlib import Path
from typing import Dict, List, Any, Tuple
    
class SystemHiddenResources:
    """Hides critical (system) resources."""
    def __init__(self, root):
        self.root = root
        
        self.mdefs: List[str] = []
        self.home: List[str] = []
        self.catalogs: List[str] = []
        self.icons: List[str] = []
        self.files: List[str] = []
        
        self.load_resources()
        
    def load_resources(self):
        hidden_dict = {}
        try:
            parent_catalog = Path(__file__).parent
            hidden_catalog = parent_catalog / 'hidden'
            
            hidden_paths = hidden_catalog / 'hidden_paths.json'
            
            with open(hidden_paths, 'r', encoding='utf-8') as file:
                hidden_dict = json.loads(file.read())
                
            self.mdefs = [path.replace('/', os.sep) for path in hidden_dict.get('mdefs') if path]
            self.home = [path.replace('/', os.sep) for path in hidden_dict.get('home') if path]
            self.catalogs = [path.replace('/', os.sep) for path in hidden_dict.get('catalogs') if path]
            self.icons = [path.replace('/', os.sep) for path in hidden_dict.get('icons') if path]
            self.files = [path.replace('/', os.sep) for path in hidden_dict.get('files') if path]

        except FileNotFoundError as e:
            showerror(
                title='Yellow Pather Error 002:',
                message='Load Error: Failed to load modules for hide',
                parent=self.root
            )
                
        except Exception as e:
            showerror(
                title='Yellow Pather Error 002:',
                message=f'Load Error: {type(e).__name__}: {e}',
                parent=self.root
            )
    
"""TODO: В будущем этот класс будет использоваться для скрытия пользовательских ресурсов."""
class UserHiddenResources:
    """Stores paths of user resources."""
    def __init__(self, root) -> None:
        self.root = root
        
        self.hidden_catalog_list: List[Path] = []
        self.hidden_file_list: List[Path] = []
        
    def add_catalog_to_list(self, path):
        try:
            if path not in self.hidden_catalog_list:
                self.hidden_catalog_list.append(path)
        except Exception as e:
            showerror(title='Yellow Pather Error 003:', message=f'Hide Error: {e}', parent=self.root)
            
    def add_file_to_list(self, path):
        try:
            if path not in self.hidden_file_list:
                self.hidden_file_list.append(path)
        except Exception as e:
            showerror(title='Yellow Pather Error 003:', message=f'Hide Error: {e}', parent=self.root)


"""TODO: Данный класс нуждается в доработке (будет перенесён в MDEFS)."""
class PermissionManager:
    """
    Manages permissions for protected directories.

    This class handles setting and managing file permissions for system
    directories based on the operating system.

    Attributes:
        protect_catalog_list: List of protected directory paths.
        system_paths: Path to system configuration file.
    """

    def __init__(self, root, os_system) -> None:
        """Initializes PermissionManager with empty protection list."""
        self.root = root
        self.os_system = os_system

        self.protect_catalog_list: List[Path] = []
        self.system_paths = None

    def set_permissions(self) -> None:
        """
        Sets directory permissions based on operating system.

        Uses ICACLS for Windows and chmod for Unix-based systems to set
        appropriate permissions on protected directories.

        Raises:
            Exception: General errors during permission setting.
            subprocess.CalledProcessError: Command execution errors.
        """
        try:
            if self.system_paths is None:
                return

            system_tuple = self.os_system.get_system()
            system = system_tuple[0]

            system_config = {}

            with open(self.system_paths, 'r', encoding='utf-8') as file:
                system_config = json.loads(file.read())

            # Windows uses ICACLS, Unix uses chmod
            if system in system_config.keys():
                for entry in self.protect_catalog_list:
                    if not entry.exists():
                        continue

                    catalog = str(entry)
                    if system == 'Windows':
                        try:
                            commands = [
                                f'icacls "{catalog}" /grant "Администраторы:(OI)(CI)F" /T /C /Q',
                                f'icacls "{catalog}" /grant "Пользователи:(OI)(CI)RX" /T /C /Q',
                                f'icacls "{catalog}" /inheritance:r /Q'
                            ]

                            for cmd in commands:
                                subprocess.run(
                                    cmd, text=True, shell=True,
                                    check=True, capture_output=True
                                )
                        except subprocess.CalledProcessError as e:
                            error_msg = (
                                f"Access rights were not set {catalog}\n\n"
                                f"Reason: {e}"
                            )
                            showerror(title='Yellow Pather Error 005:', message=error_msg, parent=self.root)

                    elif system in ['Darwin', 'Linux']:
                        # Recursively set permissions to 0o755 (rwxr-xr-x)
                        if system == 'Linux' and 'ANDROID_STORAGE' in os.environ.keys():
                            if os.getuid() != 0:
                                info_msg = (
                                    'Failed to set Android permissions\n\n'
                                    'Root permissions are not enabled\n\n'
                                    'Ignore this problem!\n\n'
                                    '!!!Never install root rights without the approriate skills!!!'
                                )
                                showinfo(
                                    title='Message:', 
                                    message=info_msg,
                                    parent=self.root)
                                return

                        for root, dirs, files in os.walk(catalog):
                            for item in dirs + files:
                                item_path = os.path.join(root, item)
                                os.chmod(item_path, 0o755)

        except Exception as e:
            showerror(title='Yellow Pather Error 004:', message=f'Permission Error: {e}', parent=self.root)


def decorator_init():
    """Initializes error handler decorator.

    Returns:
        Error handler decorator or stub if import fails.
    """
    try:
        from utils.errors.error_detector import ErrorHandler
        return ErrorHandler.handle_errors
    except ImportError:
        return create_stub_decorator()


def create_stub_decorator():
    """Creates a stub decorator for error handling.

    Returns:
        Function: Decorator that does nothing (pass-through).
    """
    def handle_errors(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return handle_errors


handle_errors = decorator_init()


class FileManagerApp:
    """
    Main file manager application class for Windows 7.

    Provides dual-pane file manager interface with navigation, search,
    and file operations in the style of classic Windows 7 Explorer.
    """

    def __init__(self, root) -> None:
        """
        Initializes file manager application.

        Args:
            root: Tkinter root window.
        """
        self.root = root
        self.root.title('Yellow Pather Explorer')
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        
        self._create_position: int = 0
        self._sort_position: int = 0
        self._start_position: int = 0
        self._root_position: int = 0

        self.counters: Dict[int] = {}
        self.states: Dict[str] = {}
        self.settings: Dict[Dict] = {}
        self.mdefs: Dict[Dict] = {}
        self.mdefs_states: Dict[Dict] = {}
        self.extensions: Dict[Dict] = {}
        self.extension_dict: Dict[Dict] = {}
  
        self._counters = {
            'start_position': self._start_position,
            'root_position': self._root_position
        }

        self._settings_counts = {
            'create_position': self._create_position,
            'sort_position': self._sort_position
        }

        self._states = {'create': 'folder', 'sorting': 'standart', 
            'protect': 'Protected'}
        self._mdefs_states = {'imported': False}

        self._extensions = {
            "languages": {
                ".c": "C", ".cpp": "C++", ".cs": "C#", ".java": "Java",
                ".js": "JavaScript", ".py": "Python", ".kt": "Kotlin"
            },
            "text": {
                ".css": "CSS", ".csv": "CSV", ".doc": "DOC",
                ".docx": "DOCX", ".html": "HTML", ".pdf": "PDF",
                ".txt": "TXT", ".log": "LOG", ".xml": "XML"
            },
            "others": {
                ".bin": "BIN", ".enc": "ENC",
                ".jar": "JAR", ".json": "JSON"
            }
        }
        
        self.parent_catalog = Path(__file__).parent
        self.config_catalog = self.parent_catalog / 'config'
        self.system_paths = self.config_catalog / 'system_paths.json'
        self.settings_configure = self.config_catalog / 'settings.json'
        self.mdefs_configure = self.config_catalog / 'mdefs.json'
        self.file_extensions = self.config_catalog / 'file_extensions.json'

        if not self.check_resource_exists(self.settings_configure):
            self.create_settings_configure(self.settings_configure)
            self.load_settings_configure()
        else:
            self.load_settings_configure()

        if not self.check_resource_exists(self.mdefs_configure):
            self.create_mdefs_configure(self.mdefs_configure)
            self.load_mdefs_configure()
        else:
            self.load_mdefs_configure()

        if not self.check_resource_exists(self.file_extensions):
            self.create_file_configure(self.file_extensions)
            self.load_file_configure()
        else:
            self.load_file_configure()

        self.check_settings_parameters()
              
        self._COMMANDS: Tuple[str] = ('cmd-parser:on', 'cmd-parser:off')

        self._system = SystemHiddenResources(self.root)

        self._globals: Dict[Any] = {
            'root': self.root,
            'counters': self.counters,
            'commands': self._COMMANDS,
            'extensions': self.extension_dict,
            'mdefs': self.mdefs,
            'states': self._states,
            'system': self._system,
            'system_paths': self.system_paths,
            'settings_counts': self._settings_counts
        }

        self.BASIC_PATH_CONFIG: Dict[str] = {
            'Windows': {'root': 'C:\\'},
            'Darwin': {'root': '/'},
            'Linux': {'root': '/'},
            'Android': {'root': '/storage/emulated/0/'},
            'auto_detect': False,
            'root_path': False,
            'user_path': False,
            'device_path': True
        }

        self.ENVIRON_NAME: Dict[str] = {
            'ru.iiec.pydroid3': 'Pydroid3',
            'myenv': 'VSCode'
        }

        self._factory = self.factory
        
        if self._factory.statistic():
            self.load_resources()
        else:
            self.close_window()

    @property
    @lru_cache(maxsize=None)
    def factory(self):
        from protect.services.factory import Factory
        return Factory(self._globals, main=self)

    def check_settings_parameters(self):
        if self._settings_counts['create_position'] <= -1:
            self._settings_counts['create_position'] = 0

        if self._settings_counts['create_position'] >= 2:
            self._settings_counts['create_position'] = 1

        if self._settings_counts['sort_position'] <= -1:
            self._settings_counts['sort_position'] = 0

        if self._settings_counts['sort_position'] >= 4:
            self._settings_counts['sort_position'] = 3

        if not isinstance(self._settings_counts['create_position'], int):
            self._settings_counts['create_position'] = 0

        if not isinstance(self._settings_counts['sort_position'], int):
            self._settings_counts['sort_position'] = 0

    def load_resources(self) -> None:
        """
        Loads application resources and creates directory structure.

        Raises:
            Exception: If resource loading fails.
        """
        try:
            self._factory.app_gui.widgets_container()
            self._factory.app_gui.create_interface()
            self._factory.main_events.bind_events()
        
            parent_catalog = Path(__file__).parent
            program_name = ''

            perms = self._factory.app_perms.permission_detector(parent_catalog)
            variables = ('VIRTUAL_ENV', 'HOME')
            home_path = Path(self.environ_manager(variables))
            home_name = str(home_path.parent.name)

            if home_name in self.ENVIRON_NAME:
                program_name = self.ENVIRON_NAME.get(home_name)
            else:
                program_name = 'System'

            error_msg = (
                f"'{parent_catalog.name}' denies access right '{program_name}'\n\n"
                f"Reason: Permissions not are set\n\n"
                f"Help:\n\n"
                f"• For Windows: iCACLS '{parent_catalog.name}' "
                f"/grant \"Everyone:(OI)(CI)F\"\n\n"
                f"• For MacOS/Linux: chmod 777 '{parent_catalog.name}' "
                f"(current: {perms})"
            )

            if not self._factory.app_perms.check_permission(parent_catalog) and not self._factory.app_state.no_message_show:
                showerror(title='Yellow Pather Error 011:', message=error_msg, parent=self.root)
                self.close_window()
                return

            if not self.check_resource_exists(self.system_paths):
                self.create_basic_path_config(self.system_paths)

            self._factory.redactor_core.load_resources(parent_catalog)
            self._factory.parser_core.load_resources(parent_catalog)

            #self._perms.system_paths = self.system_paths
            #protect_path = parent_catalog.parents[0]
            #self._perms.protect_catalog_list.append(protect_path)
            #self._perms.set_permissions()

            self._factory.path_analyzer.search_path()
        except Exception as e:
            showerror(title='Yellow Pather Error 002:', 
                message=f'Load Error: {e}', parent=self.root)

    def environ_manager(self, variables: tuple) -> str:
        """
        Gets environment variables.

        Args:
            variables: Tuple of environment variable names to search.

        Returns:
            Value of found environment variable or empty string.

        Raises:
            Exception: If environment access fails.
        """
        try:
            environ_dictionary = os.environ

            for variable in variables:
                if variable in environ_dictionary:
                    return environ_dictionary.get(variable)
            return ''
        except Exception as e:
            showerror(title='Yellow Pather Error 008:', 
                message=f'Environ Error: {e}', parent=self.root)

    @handle_errors
    def check_resource_exists(self, check_path: Path) -> bool:
        """
        Checks if a file exists.

        Args:
            check_path: File path to check.

        Returns:
            True if file exists, shows info message if not.
        """
        if not check_path.exists():
            showinfo(
                title='Message:',
                message=f"'{check_path.name}' will be created",
                parent=self.root
            )
            return False
        return True

    @handle_errors
    def create_basic_path_config(self, config_path: Path) -> None:
        """
        Creates basic path configuration file.

        Args:
            config_path: Path where config file should be created.
        """
        with open(config_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.BASIC_PATH_CONFIG, json_file, indent=4)

    @handle_errors
    def create_settings_configure(self, config_path: Path):
        with open(config_path, 'w', encoding='utf-8') as json_file:
            data = {'counters': self._settings_counts, 'states': self._states}
            json.dump(data, json_file, indent=4)

    @handle_errors
    def load_settings_configure(self):
        with open(self.settings_configure, 'r', encoding='utf-8') as json_file:
            self.settings = json.loads(json_file.read())
            self.settings_counts = self.settings['counters']
            self.states = self.settings['states']

    @handle_errors
    def create_mdefs_configure(self, config_path: Path):
        with open(config_path, 'w', encoding='utf-8') as json_file:
            data = {'states': self._mdefs_states}
            json.dump(data, json_file, indent=4)

    @handle_errors
    def load_mdefs_configure(self):
        with open(self.mdefs_configure, 'r', encoding='utf-8') as json_file:
            self.mdefs = json.loads(json_file.read())
            self.mdefs_states = self.mdefs['states']

    @handle_errors
    def create_file_configure(self, config_path: Path):
        with open(config_path, 'w', encoding='utf-8') as json_file:
            data = {'extensions': self._extensions}
            json.dump(data, json_file, indent=4)

    @handle_errors
    def load_file_configure(self):
        with open(self.file_extensions, 'r', encoding='utf-8') as json_file:
            self.extensions = json.loads(json_file.read())
            self.extension_dict = self.extensions['extensions']

    def close_window(self) -> None:
        """Closes application and all additional windows."""
        self._settings_counts = self.settings_counts
        self._states = self.states
        try:
            if self.check_resource_exists(self.settings_configure):
                self.create_settings_configure(self.settings_configure)
        except Exception:
            pass

        if (self._factory.settings_core.settings_window and 
            self._factory.settings_core.settings_window.winfo_exists()):
            self._factory.settings_core.close_window()

        if self.root and self.root.winfo_exists():
            self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

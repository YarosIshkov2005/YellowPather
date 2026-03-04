# Standard libraries
import json
import os
import subprocess
import textwrap
import traceback

# Third-party libraries
import tkinter as tk
from tkinter.messagebox import showinfo, showerror

# Local modules
from functools import wraps, lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MDEFSFramework:
    """Initializes MDEFS."""
    def __init__(self, root, app_gui, app_state, app_perms, path_manager, search, select_state, select_position, app_render) -> None:
        self.root = root
        self.app_gui = app_gui
        self.app_state = app_state
        self.app_perms = app_perms
        self.path_manager = path_manager
        self.search = search
        self.select_state = select_state
        self.select_position = select_position
        self.app_render = app_render
        
        self._mdefs_framework = self.mdefs_framework

    @property
    @lru_cache(maxsize=None)
    def mdefs_framework(self):
        from protect.mdefs.mdefs import MDEFSManager
        return MDEFSManager(
            root=self.root, 
            app_gui=self.app_gui, 
            app_state=self.app_state, 
            app_perms=self.app_perms,
            path_manager=self.path_manager, 
            search=self.search, 
            select_state=self.select_state, 
            select_position=self.select_position, 
            app_render=self.app_render
        )

    
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


class ImportManager:
    """
    Manages import of command parser modules.

    This class handles dynamic import of command detection and execution
    modules from specified directories, managing the import state.

    Attributes:
        state (AppState): Application state manager.
        command_detector_core: Imported CommandDetectorCore module.
        command_executer_core: Imported CommandExecuterCore module.
    """

    def __init__(self) -> None:
        """Initializes ImportManager with application state."""
        pass

    def os_system(self, root, system_paths):
        from system.os_system import SystemDetector
        return SystemDetector(root=root, system_paths=system_paths)
        
    def app_state(self):
        from core.state.main.app_state import AppState
        return AppState()
        
    def perms_state(self):
        from core.state.main.app_state import PermissionState
        return PermissionState()

    def secure_state(self):
        from core.state.main.app_state import SecureState
        return SecureState()

    def select_state(self, app_gui):
        from core.state.select.select_state import SelectPosition
        return SelectPosition(app_gui=app_gui)

    def select_position(self, app_gui, path_manager):
        from core.select.select_position import SelectPosition
        return SelectPosition(app_gui=app_gui, path_manager=path_manager)
        
    def app_perms(self, root, os_system, app_gui, app_state, perms_state, select_state, secure_manager, button_state, path_manager, app_render, counters, commands):
        from core.perms.check_permissions import CheckPermissionsCore
        return CheckPermissionsCore(root=root, os_system=os_system, app_gui=app_gui, app_state=app_state, perms_state=perms_state, select_state=select_state, secure_manager=secure_manager, button_state=button_state, path_manager=path_manager, app_render=app_render, counters=counters, commands=commands)
        
    def app_navigator(self, root, counters, search, app_gui, app_state, select_state, button_state, mdefs, select_position, secure_manager, app_render, app_perms, path_manager, input_manager, catalog_detector, path_analyzer):
        from managers.navigation.app_navigator import AppNavigatorCore
        return AppNavigatorCore(counters=counters, root=root, search=search, app_gui=app_gui, app_state=app_state, select_state=select_state, button_state=button_state, mdefs=mdefs, select_position=select_position, secure_manager=secure_manager, app_render=app_render, app_perms=app_perms, path_manager=path_manager, input_manager=input_manager, catalog_detector=catalog_detector, path_analyzer=path_analyzer)
        
    def path_manager(self):
        from managers.paths.path_manager import PathManager
        return PathManager()
        
    def command_detector(self, root, commands) -> None:
        """
        Imports CommandDetector from specified directory.

        Args:
            root (tk.Tk): Main window.
        """
        from components.parser.command_detector import CommandDetectorCore
        return CommandDetectorCore(root=root, commands=commands)

    def command_executer(self, root):
        from components.parser.command_executer import CommandExecuterCore
        return CommandExecuterCore(root=root)
        
    def command_parser(self, root, counters, select_position, app_render, mdefs, parser, app_gui, app_state, search, button_state, path_manager, commands):
        from managers.parser.command_parser import CommandParserCore
        return CommandParserCore(
            root=root,
            counters=counters, 
            select_position=select_position,
            app_render=app_render, 
            mdefs=mdefs, 
            parser=parser, 
            app_gui=app_gui, 
            app_state=app_state, 
            search=search,
            button_state=button_state,
            path_manager=path_manager, 
            commands=commands
        )
        
    def app_render(self, root, counters, app_gui, app_state, select_position, select_state, button_state, path_manager):
        from core.render.main.app_render import AppRenderCore
        return AppRenderCore(
            counters=counters,
            root=root,
            app_gui=app_gui,
            app_state=app_state,
            select_position=select_position,
            select_state=select_state,
            button_state=button_state,
            path_manager=path_manager
        )
        
    def button_state(self, app_gui, app_state, path_manager, select_position):
        from core.state.button.button_state import ButtonState
        return ButtonState(
            app_gui=app_gui,
            app_state=app_state,
            path_manager=path_manager,
            select_position=select_position
        )

    def update_gui(self, app_gui, app_state, app_render, app_navigator, button_state, select_position):
        from core.render.update.update_gui import UpdateGUI
        return UpdateGUI(app_gui=app_gui, app_state=app_state, app_render=app_render, app_navigator=app_navigator, button_state=button_state, select_position=select_position)
        
    def keyboard(self, path_analyzer, app_navigator, update_gui):
        from controllers.hotkeys.shortcut_dispather import PressControllerCore
        return PressControllerCore(path_analyzer=path_analyzer, app_navigator=app_navigator, update_gui=update_gui)

    def secure_manager(self, counters, root, os_system, app_gui, app_state, button_state, secure_state, system):
        from managers.secure.secure_manager import SecureManager
        return SecureManager(
            counters=counters,
            root=root,
            os_system=os_system,
            app_gui=app_gui,
            app_state=app_state,
            button_state=button_state,
            secure_state=secure_state,
            system=system
        )

    def system_manager(self, root, settings, app_gui, app_state, app_perms, secure_state, system_paths, os_system, path_manager, secure_manager):
        from managers.system.system_manager import SystemManager
        return SystemManager(
            root=root,
            settings=settings,
            app_gui=app_gui,
            app_state=app_state,
            app_perms=app_perms,
            secure_state=secure_state,
            system_paths=system_paths,
            os_system=os_system,
            path_manager=path_manager,
            secure_manager=secure_manager
        )

    def input_manager(self, root, app_gui, app_state, secure_state, secure_manager, app_perms, mdefs):
        from managers.input.input_manager import InputManager
        return InputManager(
            root=root,
            app_gui=app_gui,
            app_state=app_state,
            secure_state=secure_state,
            secure_manager=secure_manager,
            app_perms=app_perms,
            mdefs=mdefs
        )

    def resource_manager(self, perms_state, app_perms):
        from managers.resources.resource_manager import ResourceManager
        return ResourceManager(perms_state=perms_state, app_perms=app_perms)

    def catalog_detector(self, root, app_gui, app_state, app_render, search, path_manager, system_manager, input_manager):
        from managers.catalogs.catalog_detector import CatalogDetector
        return CatalogDetector(root=root, app_gui=app_gui, app_state=app_state, app_render=app_render, search=search, path_manager=path_manager, system_manager=system_manager, input_manager=input_manager)

    def path_analyzer(self, root, app_gui, app_state, app_perms, secure_state, search, select_position, app_render, button_state, path_manager, catalog_detector, command_parser, secure_manager, mdefs):
        from managers.analyzer.path_analyzer import PathAnalyzer
        return PathAnalyzer(root=root, app_gui=app_gui, app_state=app_state, app_perms=app_perms, secure_state=secure_state, search=search, select_position=select_position, app_render=app_render, button_state=button_state, path_manager=path_manager, catalog_detector=catalog_detector, command_parser=command_parser, secure_manager=secure_manager, mdefs=mdefs)


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
        self.root.title('Yellow Pather v1.0.0')
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        
        self._start_position: int = 0
        self._root_position: int = 0
  
        self._counters = {
            'start_position': self._start_position,
            'root_position': self._root_position
        }
        
        self.parent_catalog = Path(__file__).parent
        self.config_catalog = self.parent_catalog / 'config'
        self.system_paths = self.config_catalog / 'system_paths.json'
              
        self._COMMANDS: Tuple[str] = ('cmd-parser:on', 'cmd-parser:off')
        
        self._importer = ImportManager()
        self._system = SystemHiddenResources(self.root)
        self._hidden = UserHiddenResources(self.root)
        
        self._app_gui = self.app_gui
        self._app_state = self._importer.app_state()
        self._perms_state = self._importer.perms_state()
        self._secure_state = self._importer.secure_state()
        self._path_manager = self._importer.path_manager()

        self._command_detector = self._importer.command_detector(self.root, self._COMMANDS)
        self._command_executer = self._importer.command_executer(self.root)
        self._parser = CommandParserInit(self.root, self._command_detector, self._command_executer)

        self._select_state = self._importer.select_state(self._app_gui)
        self._select_position = self._importer.select_position(self._app_gui, self._path_manager)
        self._button_state = self._importer.button_state(self._app_gui, self._app_state, self._path_manager, self._select_position)
        self._app_render = self._importer.app_render(self.root, self._counters, self._app_gui, self._app_state, self._select_position, self._select_state, self._button_state, self._path_manager)
        self._search = FileManagerSearch(self.root, self._system, self._path_manager, self._COMMANDS)
        self._os_system = self._importer.os_system(self.root, self.system_paths)
        self._secure_manager = self._importer.secure_manager(self._counters, self.root, self._os_system, self._app_gui, self._app_state, self._button_state, self._secure_state, self._system)
        self._app_perms = self._importer.app_perms(self.root, self._os_system, self._app_gui, self._app_state, self._perms_state, self._select_state, self._secure_manager, self._button_state, self._path_manager, self._app_render, self._counters, self._COMMANDS)
        self._mdefs = MDEFSFramework(self.root, self._app_gui, self._app_state, self._app_perms, self._path_manager, self._search, self._select_state, self._select_position, self._app_render)
        self._settings = FileManagerSettings(self.root, self._app_gui, self._app_state, self._path_manager, self._mdefs, self._search, self._app_render, self._select_position)
        #self._perms = PermissionManager(self.root, self._os_system)

        #self._resource_manager = self._importer.resource_manager(self._perms_state, self._app_perms)

        self._system_manager = self._importer.system_manager(self.root, self._settings, self._app_gui, self._app_state, self._app_perms, self._secure_state, self.system_paths, self._os_system, self._path_manager, self._secure_manager)
        self._input_manager = self._importer.input_manager(self.root, self._app_gui, self._app_state, self._secure_state, self._secure_manager, self._app_perms, self._mdefs)
        self._command_parser = self._importer.command_parser(self.root, self._counters, self._select_position, self._app_render, self._mdefs, self._parser, self._app_gui, self._app_state, self._search, self._button_state, self._path_manager, self._COMMANDS)
        self._file_redactor = FileRedactorCore(self.root, self._app_gui, self._app_perms, self._search, self._settings, self._path_manager, self._app_render)
        self._catalog_detector = self._importer.catalog_detector(self.root, self._app_gui, self._app_state, self._app_render, self._search, self._path_manager, self._system_manager, self._input_manager)
        self._path_analyzer = self._importer.path_analyzer(self.root, self._app_gui, self._app_state, self._app_perms, self._secure_state, self._search, self._select_position, self._app_render, self._button_state, self._path_manager, self._catalog_detector, self._command_parser, self._secure_manager, self._mdefs)
        self._app_navigator = self._importer.app_navigator(self.root, self._counters, self._search, self._app_gui, self._app_state, self._select_state, self._button_state, self._mdefs, self._select_position, self._secure_manager, self._app_render, self._app_perms, self._path_manager, self._input_manager, self._catalog_detector, self._path_analyzer)
        self._update_gui = self._importer.update_gui(self._app_gui, self._app_state, self._app_render, self._app_navigator, self._button_state, self._select_position)
        self._keyboard = self._importer.keyboard(self._path_analyzer, self._app_navigator, self._update_gui)
        self._main_events = self.main_events

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

        self.load_resources()

    @property
    @lru_cache(maxsize=None)
    def app_gui(self):
        from core.gui.main.app_gui import AppGUI
        return AppGUI(root=self.root)

    @property
    @lru_cache(maxsize=None)
    def main_events(self):
        from core.events.main.main_events import MainEvents
        return MainEvents(
            root=self.root, 
            app_gui=self._app_gui, 
            app_navigator=self._app_navigator, 
            app_render=self._app_render, 
            button_state=self._button_state, 
            keyboard=self._keyboard, 
            path_analyzer=self._path_analyzer, 
            settings=self._settings,
            update_gui=self._update_gui
        )

    def load_resources(self) -> None:
        """
        Loads application resources and creates directory structure.

        Raises:
            Exception: If resource loading fails.
        """
        try:
            self._app_gui.widgets_container()
            self._app_gui.create_interface()
            self._main_events.bind_events()
        
            parent_catalog = Path(__file__).parent
            program_name = ''

            perms = self._app_perms.permission_detector(parent_catalog)
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

            if not self._app_perms.check_permission(parent_catalog) and not self._app_state.no_message_show:
                showerror(title='Yellow Pather Error 011:', message=error_msg, parent=self.root)
                self.close_window()
                return

            if not self.check_resource_exists(self.system_paths) or self.system_paths.stat().st_size == 0:
                self.create_basic_path_config(self.system_paths)

            self._file_redactor.load_resources(parent_catalog)
            self._parser.load_resources(parent_catalog)

            #self._perms.system_paths = self.system_paths
            protect_path = parent_catalog.parents[0]
            #self._perms.protect_catalog_list.append(protect_path)
            #self._perms.set_permissions()

            self._path_analyzer.search_path()
        except Exception as e:
            showerror(title='Yellow Pather Error 002:', message=f'Load Error: {traceback.format_exc()}', parent=self.root)

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
            showerror(title='Yellow Pather Error 008:', message=f'Environ Error: {e}', parent=self.root)

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

    def close_window(self) -> None:
        """Closes application and all additional windows."""
        self._settings.close_window()

        if self.root and self.root.winfo_exists():
            self.root.destroy()


class FileManagerSearch:
    """
    Search and file/directory processing class.

    Provides methods for file searching, directory iteration, and
    name processing for display.
    """

    def __init__(self, root, system, path_manager, commands) -> None:
        """Initializes FileManagerSearch with empty lists."""
        self.root = root
        self.system = system
        self.path_manager = path_manager
        self.COMMANDS = commands if commands is not None else ()
        
        self.total: int = 0

    @handle_errors
    def iteration_dir(self, path: Path, protect_catalogs: Path) -> list:
        """
        Gets list of absolute paths in specified directory.

        Args:
            path: Directory to iterate.
            protect_catalogs: List of directories to exclude.

        Returns:
            List of absolute paths in directory.
        """
        path = Path(path) if isinstance(path, str) else path

        total_protects = len(protect_catalogs) - 1
        count = -1
            
        for entry in path.iterdir():
            if count < total_protects:
                count += 1

            if entry.name in self.COMMANDS:
                continue
                
            if entry.name in self.system.home:
                continue

            if entry.name in self.system.catalogs:
                continue

            path_str = str(entry)
            if len(protect_catalogs) > 0:
                protect_catalog = str(protect_catalogs[count])

                if path_str == protect_catalog:
                    continue

            self.path_manager.abs_paths.append(entry)

        self.total = len(self.path_manager.abs_paths)
        
        return self.path_manager.abs_paths

    @handle_errors
    def iteration_name(self, root_path: Path) -> list:
        """
        Gets list of relative paths from base path.

        Args:
            root_path (Path): Base path for relative calculations.

        Returns:
            List of relative paths.
        """
        if root_path is None:
            return

        for entry in self.path_manager.abs_paths:
            self.path_manager.rel_paths.append(entry.relative_to(root_path))

        return self.path_manager.rel_paths

    @handle_errors
    def iteration_short_name(self) -> list:
        """
        Generates shortened names for display.

        Returns:
            List of shortened names with ellipsis if needed.
        """
        for entry in self.path_manager.abs_paths:
            if entry.is_symlink():
                short_name = textwrap.shorten(
                    str(entry.name) + f'->{os.sep}', width=35, placeholder='...'
                )
            elif entry.is_dir():
                short_name = textwrap.shorten(
                    str(entry.name) + os.sep, width=35, placeholder='...'
                )
            elif entry.is_file():
                short_name = textwrap.shorten(
                    str(entry.name), width=35, placeholder='...'
                )
            self.path_manager.short_names.append(short_name)

        return self.path_manager.short_names

    @handle_errors
    def glob_search(self, path: Path, extension: str) -> list:
        """
        Non-recursive file search by extension.

        Args:
            path: Directory to search in.
            extension: File extension to search for.

        Returns:
            List of found file names.
        """
        self.path_manager.abs_paths.clear()
        self.path_manager.rel_paths.clear()
        self.path_manager.short_names.clear()

        for entry in path.glob(f"*{extension}"):
            self.path_manager.abs_paths.append(entry)

            short_name = textwrap.shorten(
                entry.name, width=35, placeholder='...'
            )
            self.path_manager.short_names.append(short_name)

        self.total = len(self.path_manager.short_names)
        
        return self.path_manager.short_names

    @handle_errors
    def rglob_search(self, path: Path, extension: str) -> list:
        """
        Recursive file search by extension.

        Args:
            path: Directory to search in.
            extension: File extension to search for.

        Returns:
            List of found file names.
        """
        self.path_manager.abs_paths.clear()
        self.path_manager.rel_paths.clear()
        self.path_manager.short_names.clear()

        for entry in path.rglob(f'*{extension}'):
            #if entry in protect_files:
                #continue

            root_path = str(self.path_manager.root_path)
            absolute_path = str(entry)
            resource = os.path.relpath(absolute_path, root_path)
            
            if resource in self.system.mdefs:
                continue
                
            if resource in self.system.home:
                continue
                
            if resource in self.system.catalogs:
                continue

            if resource in self.system.icons:
                continue
                
            if resource in self.system.files:
                continue
            
            self.path_manager.abs_paths.append(entry)

            short_name = textwrap.shorten(
                str(entry.name), width=35, placeholder='...'
            )
            self.path_manager.short_names.append(short_name)

        self.total = len(self.path_manager.short_names)
        
        return self.path_manager.short_names

    @handle_errors
    def add_paths(self) -> None:
        """Populates path lists for display."""
        self.path_manager.abs_paths.clear()
        self.path_manager.rel_paths.clear()
        self.path_manager.short_names.clear()

        self.path_manager.abs_paths = self.iteration_dir(self.path_manager.absolute_path, self.system.catalogs)
        self.path_manager.rel_paths = self.iteration_name(self.path_manager.root_path)
        self.path_manager.short_names = self.iteration_short_name()


class FileManagerSettings:
    """
    Application settings management class.

    Handles settings window creation, file operations, and
    extension-based file type detection.
    """

    def __init__(self, root, app_gui, app_state, path_manager, mdefs, search, app_render, select_position) -> None:
        """
        Initializes FileManagerSettings.

        Args:
            root (tk.Tk): Main Tkinter window.
            app_gui: Program GUI.
            app_state: Program state.
            path_manager: Paths for the program.
        """
        self.root = root
        self.app_gui = app_gui
        self.app_state = app_state
        self.path_manager = path_manager
        self.mdefs = mdefs
        self.search = search
        self.app_render = app_render
        self.select_position = select_position
        
        self.settings_window: Optional[tk.Tk] = None

        self._settings_gui = self.settings_gui
        self._settings_events = self.settings_events
        self._settings_manager = self.settings_manager
        self.open_file_callback = None

    @property
    @lru_cache(maxsize=None)
    def settings_gui(self):
        from core.gui.settings.settings_gui import SettingsGUI
        return SettingsGUI(settings=self)

    @property
    @lru_cache(maxsize=None)
    def settings_events(self):
        from core.events.settings.settings_events import SettingsEvents
        return SettingsEvents(settings=self, settings_gui=self._settings_gui)

    @property
    @lru_cache(maxsize=None)
    def settings_manager(self):
        from managers.settings.settings_manager import SettingsManager
        return SettingsManager(settings=self, settings_gui=self._settings_gui, mdefs=self.mdefs, search=self.search, app_render=self.app_render, select_position=self.select_position)

    def create_window(self) -> None:
        """Creates settings window."""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title('Settings')
        self.settings_window.resizable(False, False)
        self.settings_window.grab_set()
        self.settings_window.protocol('WM_DELETE_WINDOW', self.close_window)

        self._settings_gui.settings_window = self.settings_window
        self._settings_manager.settings_window = self.settings_window
        self._settings_gui.widgets_container()
        self._settings_gui.create_widgets()

        self._settings_events.bind_events()
        
        self.mdefs._mdefs_framework.callbacks['settings'] = self.settings_window
        self.control_open_button()

    @handle_errors
    def control_open_button(self) -> None:
        """Controls open button state based on selection."""
        select_path = (Path(self.path_manager.selected_path) if isinstance(
            self.path_manager.selected_path, str) else self.path_manager.selected_path)

        if select_path is None:
            self._settings_gui.open_button.config(state='disabled')
            self._settings_gui.create_button.config(state='normal')
            return

        if select_path.is_file():
            self._settings_gui.open_button.config(state='normal')
            self._settings_gui.create_button.config(state='disable')
        else:
            self._settings_gui.open_button.config(state='disabled')
            self._settings_gui.create_button.config(state='normal')

    def show_error(self) -> None:
        """Shows module not found error."""
        showerror(
            title='Yellow Pather Error 015:',
            message='Module Error: The operation was canceled. The module was not found',
            parent=self.root
        )

    def close_window(self) -> None:
        """Closes settings window."""
        if self.settings_window:
            self.settings_window.grab_release()
            self.settings_window.destroy()
            self.settings_window = None

        if self.root and self.root.winfo_exists():
            self.root.lift()
            self.root.focus_force()
            self.app_gui.path_entry.focus()


class CommandParserInit:
    """
    Command parser initialization class.

    Manages command parser module loading and directory structure
    for command parsing functionality.
    """

    def __init__(self, root, command_detector, command_executer) -> None:
        """Initializes CommandParserInit with managers."""
        self.root = root
        self.command_detector = command_detector
        self.command_executer = command_executer
        
    @handle_errors
    def load_resources(self, parent_path: Path) -> None:
        """Creates command parser directory structure."""
        if not self.command_detector:
            showerror(
                title='Yellow Pather Error 001:',
                message='Import Error: Failed to import command parser modules',
                parent=self.root
            )
        if not self.command_executer:
            showerror(
                title='Yellow Pather Error 001:',
                message='Import Error: Failed to import command parser modules',
                parent=self.root
            )

    @handle_errors
    def call_detector(self, cmd: str, root: Path, paths: List[Path]) -> bool:
        """
        Calls command detector module.

        Args:
            cmd: Command string to parse.
            root: Root window.
            paths: Available paths for command.

        Returns:
            True if command detection successful.
        """
        if not self.command_detector:
            self.show_error()
            return False
            
        if not hasattr(self, 'command_detector'):
            self.show_error()
            return

        return self.command_detector.parse_command_structure(cmd, root, paths)

    @handle_errors
    def call_executer(self, parameters: str) -> bool:
        """
        Calls command executor module.

        Args:
            parameters: Command parameters to execute.

        Returns:
            True if command execution successful.
        """
        if not self.command_executer:
            self.show_error()
            return False

        if not hasattr(self, 'command_executer'):
            self.show_error()
            return False

        return self.command_executer.command_executer(parameters)

    def show_error(self):
        """Shows module not found error."""
        showerror(
            title='Yellow Pather Error 015:',
            message="Module Error: The operation was canceled. The module was not found",
            parent=self.root
        )

class FileRedactorCore:
    def __init__(self, root, app_gui, app_perms, search, settings, path_manager, app_render) -> None:
        self.root = root
        self.app_gui = app_gui
        self.app_perms = app_perms
        self.search = search
        self.settings = settings
        self.path_manager = path_manager
        self.app_render = app_render

        self._file_redactor = self.file_redactor

    @property
    @lru_cache(maxsize=None)
    def file_redactor(self):
        """
        Imports FileRedactor module from specified directory.

        Args:
            catalog_path: Path to directory containing file redactor module.

        Raises:
            ModuleNotFoundError: If required module is not found in the path.
        """
        from components.redactor.file_redactor import FileRedactorCore
        return FileRedactorCore(
            root=self.root,
            app_gui=self.app_gui,
            search=self.search,
            settings=self.settings,
            path_manager=self.path_manager,
            app_render=self.app_render
        )

    @handle_errors
    def load_resources(self, parent_path: Path) -> None:
        """Creates settings directory structure."""
        parent_catalog = parent_path

        if not self.file_redactor:
            showerror(
                title='Yellow Pather Error 001:',
                message='Import Error: Failed to import FileRedactor module'
            )
            return

        icons_catalog = parent_catalog / 'icons'
        extension_catalog = parent_catalog / 'config'

        self.file_redactor.icons_path = icons_catalog
        self.file_redactor.file_extensions = extension_catalog / 'file_extensions.json'

        self.settings.open_file_callback = self.open_file_callback

    @handle_errors
    def open_file_callback(self) -> None:
        """Callback for opening selected file."""
        select_path = Path(self.path_manager.selected_path) if isinstance(self.path_manager.selected_path, str) else self.path_manager.selected_path

        if not self.app_perms.check_perms(select_path):
            return

        self.open_file(select_path)

    @handle_errors
    def open_file(self, select_path):
        """
        Opens selected file (stub method).

        Args:
            path: Path to file to open.
        """
        if not self.file_redactor:
            self.show_error()
            self.close_window()
            return

        if not hasattr(self, 'file_redactor'):
            self.show_error()
            return

        self.file_redactor.settings_window = self.settings.settings_window
        self.file_redactor.create_window(
            self.settings.settings_window
        )

        if select_path is None:
            return

        self.file_redactor.file_path = select_path
        self.file_redactor.set_icon_image()


if __name__ == '__main__':
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

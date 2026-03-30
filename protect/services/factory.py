from tkinter.messagebox import askyesno

from functools import lru_cache
from typing import Dict, List, Set

class Factory:
    def __init__(self, globals, main) -> None:
        self._globals = globals
        self._main = main

        self._root = self._globals['root']
        self._states: int = self._globals['states']
        self._settings_counts: int = self._globals['settings_counts']

        self._factories: Dict = {}
        self._instances: Dict = {}
        self._errors: Dict = {}

        self._imported: int = 0
        self._failed: int = 0

        self._registering: Set = set()

    def register(self, name, getter):
        self._factories[name] = getter

    def __getattr__(self, name):
        if name in self._instances:
            return self._instances[name]

        if name in self._registering:
            self._failed += 1
            self._errors[name] = f"Maximum recursive depth exceeded: '{name}'"
            return None

        if name not in self._factories:
            self._failed += 1
            self._errors[name] = f"'{name}' not registered"
            return None

        self._registering.add(name)
        try:
            instance = self._factories[name]()
            self._instances[name] = instance
            self._imported += 1
            return instance
        except ModuleNotFoundError:
            self._failed += 1
            self._errors[name] = f"'{name}' not found or does not exist"
            return None
        finally:
            self._registering.remove(name)

    def statistic(self):
        if self._failed == 0:
            return True

        lines = [f"Failed: '{name}' reason: '{reason}'." for name, reason in self._errors.items()]
        error_msg = "\n".join(lines)
        message = (
            'Errors occurred during import:\n\n'
            f'{error_msg}\n\n'
            f'Imported: {self._imported} modules\n'
            f'Total failed: {self._failed}\n\n'
            'Do you want to continue (YellowPather may not work properly)?'
        )
        result = askyesno(title='Yellow Pather Error 001:', message=message, 
            parent=self._root)
        return result

    @property
    @lru_cache(maxsize=None)
    def app_gui(self):
        from core.gui.main.app_gui import AppGUI
        return AppGUI(globals=self._globals)

    @property
    @lru_cache(maxsize=None)
    def app_state(self):
        from core.state.main.app_state import AppState
        return AppState()

    @property
    @lru_cache(maxsize=None)
    def perms_state(self):
        from core.state.main.app_state import PermissionState
        return PermissionState()

    @property
    @lru_cache(maxsize=None)
    def secure_state(self):
        from core.state.main.app_state import SecureState
        return SecureState()

    @property
    @lru_cache(maxsize=None)
    def select_state(self):
        from core.state.select.select_state import SelectPosition
        return SelectPosition(globals=self._globals)

    @property
    @lru_cache(maxsize=None)
    def path_manager(self):
        from managers.paths.path_manager import PathManager
        return PathManager()

    @property
    @lru_cache(maxsize=None)
    def command_detector(self):
        from components.parser.command_detector import CommandDetectorCore
        return CommandDetectorCore(globals=self._globals)

    @property
    @lru_cache(maxsize=None)
    def command_executer(self):
        from components.parser.command_executer import CommandExecuterCore
        return CommandExecuterCore(globals=self._globals)

    @property
    @lru_cache(maxsize=None)
    def parser_core(self):
        from core.parser.parser import CommandParserCore
        return CommandParserCore(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def select_position(self):
        from core.select.select_position import SelectPosition
        return SelectPosition(callstack=self)

    @property
    @lru_cache(maxsize=None)
    def button_state(self):
        from core.state.button.button_state import ButtonState
        return ButtonState(callstack=self)

    @property
    @lru_cache(maxsize=None)
    def app_render(self):
        from core.render.main.app_render import AppRenderCore
        return AppRenderCore(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def os_system(self):
        from system.os_system import SystemDetector
        return SystemDetector(globals=self._globals)

    @property
    @lru_cache(maxsize=None)
    def secure_manager(self):
        from managers.secure.secure_manager import SecureManager
        return SecureManager(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def app_perms(self):
        from core.perms.check_permissions import CheckPermissionsCore
        return CheckPermissionsCore(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def search_manager(self):
        from managers.search.search_manager import SearchManager
        return SearchManager(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def framework(self):
        from protect.framework.framework import MDEFSFramework
        return MDEFSFramework(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def settings_core(self):
        from core.settings.settings import SettingsCore
        return SettingsCore(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def command_parser(self):
        from managers.parser.command_parser import CommandParserCore
        return CommandParserCore(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def system_manager(self):
        from managers.system.system_manager import SystemManager
        return SystemManager(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def input_manager(self):
        from managers.input.input_manager import InputManager
        return InputManager(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def redactor_core(self):
        from core.redactor.redactor import FileRedactorCore
        return FileRedactorCore(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def catalog_detector(self):
        from managers.catalogs.catalog_detector import CatalogDetector
        return CatalogDetector(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def path_analyzer(self):
        from managers.analyzer.path_analyzer import PathAnalyzer
        return PathAnalyzer(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def app_navigator(self):
        from managers.navigation.app_navigator import AppNavigatorCore
        return AppNavigatorCore(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def update_gui(self):
        from core.render.update.update_gui import UpdateGUI
        return UpdateGUI(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def keyboard(self):
        from controllers.hotkeys.shortcut_dispather import PressControllerCore
        return PressControllerCore(callstack=self)

    @property
    @lru_cache(maxsize=None)
    def main_events(self):
        from core.events.main.main_events import MainEvents
        return MainEvents(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def reset_manager(self):
        from core.reset.reset_manager import ResetManager
        return ResetManager(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def resource_manager(self):
        from managers.resources.resource_manager import ResourceManager
        return ResourceManager()

    @property
    @lru_cache(maxsize=None)
    def path_canonize(self):
        from core.paths.path_canonize import PathCanonize
        return PathCanonize(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def insert_manager(self):
        from core.insert.insert_manager import InsertManager
        return InsertManager(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def configure_manager(self):
        from protect.init.configure_manager import ConfigureManager
        return ConfigureManager(callstack=self)

    @property
    @lru_cache(maxsize=None)
    def root_manager(self):
        from protect.root.paths.root_path import RootPath
        return RootPath(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def update_positions(self):
        from core.update.update_positions import UpdatePositions
        return UpdatePositions(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def breadcrumbs(self):
        from core.points.breadcrumbs import Breadcrumbs
        return Breadcrumbs(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def history_manager(self):
        from core.history.history_manager import HistoryManager
        return HistoryManager(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def update_paths(self):
        from core.updatepaths.update_paths import UpdatePaths
        return UpdatePaths(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def transitions(self):
        from core.navigation.transitions import Transitions
        return Transitions(globals=self._globals, callstack=self)

    @property
    @lru_cache(maxsize=None)
    def update_resources(self):
        from core.update.update_resources import UpdateResources
        return UpdateResources(callstack=self)

    @property
    @lru_cache(maxsize=None)
    def event_manager(self):
        from managers.events.event_manager import EventManager
        return EventManager(callstack=self)

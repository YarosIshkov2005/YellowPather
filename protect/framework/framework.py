from functools import lru_cache

class MDEFSFramework:
    """Initializes MDEFS."""
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.app_perms = self.callstack.app_perms
        self.app_render = self.callstack.app_render
        self.COMMANDS = self.globals['commands']
        self.perms_state = self.callstack.perms_state
        self.path_manager = self.callstack.path_manager
        self.search = self.callstack.search_manager
        self.system = self.globals['system']
        self.select_state = self.callstack.select_state
        self.select_position = self.callstack.select_position
        
        self._mdefs_framework = self.mdefs_framework

    @property
    @lru_cache(maxsize=None)
    def mdefs_framework(self):
        from protect.mdefs.mdefs import MDEFSManager
        return MDEFSManager(globals=self.globals, callstack=self.callstack)

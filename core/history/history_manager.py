class HistoryManager:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.app_state = self.callstack.app_state
        self.select_state = self.callstack.select_state

    def set(self, command: str = 'current', index: int = 0):
        if command != 'current' and not self.app_state.toggle_button_active:
            return

        self.select_state.pop_back_point()
        self.select_state.add_next_point(index)
        self.globals['positions']['index'] = index

    def push(self, index: int = 0):
        self.select_state.add_next_point(index)
        self.globals['positions']['index'] = index

    def pop(self):
        current = self.select_state.pop_back_point()
        self.globals['positions']['index'] = current

    def reset(self):
        self.select_state.reset_points()
        self.globals['positions']['index'] = 0
class UpdateGUI:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.button_state = self.callstack.button_state
        self.canonizer = self.callstack.path_canonize
        self.path_manager = self.callstack.path_manager
        self.select_position = self.callstack.select_position

    def update_gui(self):
        if not self.app_state.block_when_update:
            self.app_state.block_when_update = True
            
        self.app_gui.select_button.config(text='Drop')

        self.canonizer.canonizer('render')

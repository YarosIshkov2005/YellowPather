class UpdatePositions:
    def __init__(self, globals, callstack) -> None:
        self.globals = globals
        self.callstack = callstack

        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.button_state = self.callstack.button_state
        self.path_manager = self.callstack.path_manager
        self.select_state = self.callstack.select_state
        self.select_position = self.callstack.select_position

        self.current: int = 0
        self.resources: int = 0

    def update_position(self):
        element = self.globals['positions']['index']
        self.current = element + 1
        self.resources = self.return_resources()

        self.reset_states()
        self.update_states()
        self.update_marker()

        if self.path_manager.short_names:
            self.app_gui.select_window.see(element)
            self.app_gui.select_window.selection_set(element)

            if self.app_state.block_when_update:
                self.app_state.block_when_update = False
                return True
            return False

    def return_resources(self):
        resources = len(self.path_manager.short_names)
        if resources == 0:
            self.current = 0
            
        self.app_gui.elements_label.config(text=f'Elements: {resources}')
        self.app_gui.current_label.config(
            text=f'Element: {self.current}/{resources}')

        return resources

    def update_marker(self):
        if (self.app_state.reset_button_active or 
            self.app_state.next_button_active):
            self.current = 1
            self.app_gui.select_button.config(text='Select')
            self.app_gui.select_window.config(selectbackground='blue')
            
        elif self.app_state.back_button_active:
            self.current = self.globals['positions']['index']
            self.app_gui.select_button.config(text='Select')
            self.app_gui.select_window.config(selectbackground='blue')

        elif self.app_state.block_when_update:
            self.current = 1
            self.app_gui.select_button.config(text='Select')
            self.app_gui.select_window.config(selectbackground='blue')

    def reset_states(self):
        if self.app_state.search_button_active:
            self.app_state.search_button_active = False
        elif self.app_state.settings_button_active:
            self.app_state.settings_button_active = False
        elif self.app_state.toggle_button_active:
            self.app_state.toggle_button_active = False
        elif self.app_state.back_button_active:
            self.app_state.back_button_active = False
        elif self.app_state.next_button_active:
            self.app_state.next_button_active = False

    def update_states(self):
        element = self.globals['positions']['index']
        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        self.select_position.selected_index = element
        self.select_position.select_position()

        self.button_state.index = element
        self.button_state.control_update_button()
        self.button_state.control_up_button()
        self.button_state.control_select_button()
        self.button_state.control_down_button()

        self.button_state.control_back_button()
        self.button_state.control_next_button()
        self.button_state.control_settings_button()
        self.button_state.update_search_state()

    def update_index(self):
        element = self.globals['positions']['index']
        self.current = element + 1
        self.resources = self.return_resources()
        self.app_gui.current_label.config(
            text=f'Element: {self.current}/{self.resources}')

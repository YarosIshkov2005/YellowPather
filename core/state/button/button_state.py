class ButtonState:
    def __init__(self, callstack):
        self.callstack = callstack

        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.path_manager = self.callstack.path_manager
        self.select_position = self.callstack.select_position

        self.last_search_text: str = ''
        self.index: int = 0

    def control_search_button(self, event=None) -> None:
        """Controls search button state based on text changes."""
        current_path = self.app_gui.path_entry.get()

        if current_path != self.last_search_text:
            self.app_gui.search_button.config(state='normal')
            self.app_state.control_enter_search = True
        else:
            self.app_gui.search_button.config(state='disabled')
            self.app_state.control_enter_search = False

    def update_search_state(self) -> None:
        """Updates search state after path entry changes."""
        self.last_search_text = self.app_gui.path_entry.get()
        self.control_search_button()

    def control_update_button(self):
        root_path = self.path_manager.root_path

        if len(self.path_manager.short_names) <= 1:
            self.app_gui.update_button.config(state='disabled')
            return

        if root_path is not None and root_path.exists():
            self.app_gui.update_button.config(state='normal')
        else:
            self.app_gui.update_button.config(state='disabled')

    def control_up_button(self):
        if self.index != 0 and len(self.path_manager.short_names) >= 2:
            self.app_gui.up_button.config(state='normal')
        else:
            self.app_gui.up_button.config(state='disabled')

    def control_select_button(self):
        """Controls select buttons state."""
        current_path = self.select_position.absolute_path
        
        if current_path is None:
            self.app_gui.select_button.config(state='disabled')
            return

        if self.app_state.is_parser_active:
            self.app_gui.select_button.config(state='disabled')
            return

        if (self.app_state.is_recursive_search 
            and self.app_state.search_protect_enabled):
            self.app_gui.select_button.config(state='disabled')
            return

        if current_path.is_file():
            self.app_gui.select_button.config(state='normal')
        else:
            self.app_gui.select_button.config(state='disabled')

    def control_down_button(self):
        if (len(self.path_manager.short_names) >= 2 
            and self.index != len(self.path_manager.short_names) - 1):
            self.app_gui.down_button.config(state='normal')
        else:
            self.app_gui.down_button.config(state='disabled')

    def control_back_button(self) -> None:
        """Controls back button state based on navigation."""
        absolute_path = self.path_manager.absolute_path

        if not absolute_path.exists():
            self.app_gui.back_button.config(state='disabled')
            return

        if not absolute_path.samefile(self.path_manager.root_path):
            self.app_gui.back_button.config(state='normal')
        else:
            self.app_gui.back_button.config(state='disabled')
        
    def control_next_button(self) -> None:
        """Controls next button state based on directory contents."""
        current_path = self.select_position.absolute_path

        if (self.app_state.is_recursive_search 
            and self.app_state.search_protect_enabled):
            self.app_gui.next_button.config(state='disabled')
            return

        if self.app_state.is_parser_active:
            self.app_gui.next_button.config(state='disabled')
            return

        if len(self.path_manager.short_names) == 0:
            self.app_gui.next_button.config(state='disabled')
            return

        if not current_path.is_file():
            self.app_gui.next_button.config(state='normal')
        else:
            self.app_gui.next_button.config(state='disabled')

    def control_settings_button(self):
        if self.path_manager.root_path is None:
            self.app_gui.settings_button.config(state='disabled')
            return

        if self.app_state.is_parser_active:
            self.app_gui.settings_button.config(state='disabled')
            return
            
        if (not self.app_state.is_recursive_search 
            or not self.app_state.search_protect_enabled):
            self.app_gui.settings_button.config(state='normal')
        else:
            self.app_gui.settings_button.config(state='disabled')


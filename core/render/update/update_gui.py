class UpdateGUI:
    def __init__(self, app_gui, app_state, app_render, app_navigator, select_position) -> None:
        self.app_gui = app_gui
        self.app_state = app_state
        self.app_render = app_render
        self.app_navigator = app_navigator
        self.select_position = select_position

    def update_gui(self):
        if not self.app_state.block_when_update:
            self.app_state.block_when_update = True
            
        self.app_gui.select_button.config(text='Drop')
        self.app_navigator.index = 0
        self.app_navigator.marker_select()
        self.app_render.update_select_window()

        self.select_position.selected_index = self.app_navigator.index
        self.select_position.select_position()

        absolute_path = self.select_position.absolute_path.parent
        self.app_render.canonize_entered_path(absolute_path)

class PressControllerCore:
    def __init__(self, callstack):
        self.callstack = callstack

        self.app_navigator = self.callstack.app_navigator
        self.path_analyzer = self.callstack.path_analyzer
        self.update_gui = self.callstack.update_gui

    def search_path_callback(self, event=None):
        self.app_navigator.directory_down()

    def reset_path_callback(self, event=None):
        self.app_navigator.reset_path()

    def marker_up_callback(self, event=None):
        self.app_navigator.marker_up()

    def marker_select_callback(self, event=None):
        self.app_navigator.marker_select()

    def marker_down_callback(self, event=None):
        self.app_navigator.marker_down()

    def directory_up_callback(self, event=None):
        self.app_navigator.directory_up()

    def directory_down_callback(self, event=None):
        self.app_navigator.directory_down()

    def update_gui_callback(self, event=None):
        self.update_gui.update_gui()

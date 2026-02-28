class PressControllerCore:
    def __init__(self, path_analyzer, app_navigator, update_gui):
        self.path_analyzer = path_analyzer
        self.app_navigator = app_navigator
        self.update_gui = update_gui

    def search_path_callback(self, event=None):
        self.path_analyzer.search_path()

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

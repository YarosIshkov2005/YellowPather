class SettingsEvents:
    def __init__(self, settings, settings_gui) -> None:
        self.settings = settings
        self.settings_gui = settings_gui

    def bind_events(self):
        self.settings_gui.open_button.config(command=self.settings.open_file_callback)
        self.settings_gui.exit_button.config(command=self.settings.close_window)
        self.settings_gui.back_button.config(command=self.settings._settings_manager.back_type)
        self.settings_gui.next_button.config(command=self.settings._settings_manager.next_type)
        self.settings_gui.create_button.config(command=lambda: self.settings._settings_manager.create_rename_window('create'))
        self.settings_gui.delete_button.config(command=self.settings._settings_manager.delete_select_resource)
        self.settings_gui.rename_button.config(command=lambda: self.settings._settings_manager.create_rename_window('rename'))
        self.settings_gui.left_button.config(command=self.settings._settings_manager.select_back_sort)
        self.settings_gui.right_button.config(command=self.settings._settings_manager.select_next_sort)
        self.settings_gui.radiobutton_1.config(command=self.settings._settings_manager.protect_on)
        self.settings_gui.radiobutton_2.config(command=self.settings._settings_manager.protect_off)
        self.settings_gui.radiobutton_3.config(command=self.settings._settings_manager.insert_on)
        self.settings_gui.radiobutton_4.config(command=self.settings._settings_manager.insert_off)

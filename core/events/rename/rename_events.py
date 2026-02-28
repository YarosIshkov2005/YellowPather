class RenameEvents:
    def __init__(self, rename, rename_gui) -> None:
        self.rename = rename
        self.rename_gui = rename_gui

    def bind_events(self):
        self.rename_gui.cancel_button.config(command=self.rename.close_window)
        self.rename_gui.next_button.config(command=self.rename.create_method_callback)

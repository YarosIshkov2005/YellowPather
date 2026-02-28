class ProgressEvents:
    def __init__(self, progress_window, progress_gui) -> None:
        self.progress_window = progress_window
        self.progress_gui = progress_gui

    def bind_events(self):
        self.progress_gui.cancel_button.config(command=self.progress_window.cancel_operation)

class RedactorEvents:
    def __init__(self, file_redactor, redactor_gui) -> None:
        self.file_redactor = file_redactor
        self.redactor_gui = redactor_gui

    def bind_events(self):
        self.redactor_gui.text_widget.bind('<KeyRelease>', self.file_redactor.control_clear_button)
        
        self.redactor_gui.icon_label.config(image=self.file_redactor.icon_image)
        self.redactor_gui.exit_button.config(command=self.file_redactor.close_window)
        self.redactor_gui.clear_button.config(command=self.file_redactor.clear_file_data)
        self.redactor_gui.save_button.config(command=self.file_redactor.save_file_data)
